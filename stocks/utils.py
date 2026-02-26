import yfinance as yf
from django.utils import timezone
from datetime import timedelta
from .models import Stock, MonthlyData
import pandas as pd

def normalize_stock_code(code):
    code = str(code).strip()
    if code.isdigit():
        return f"{code}.T"
    return code

def get_stock_data(code):
    normalized_code = normalize_stock_code(code)

    # Check if stock exists in DB and is up to date
    stock, created = Stock.objects.get_or_create(code=normalized_code)

    now = timezone.now()
    if not created and stock.last_updated > now - timedelta(days=1) and stock.monthly_data.exists():
        return stock, None

    # Fetch from yfinance
    ticker = yf.Ticker(normalized_code)
    try:
        info = ticker.info
        if not info or ('longName' not in info and 'shortName' not in info):
            # Try to see if history works anyway
            hist = ticker.history(period="1mo")
            if hist.empty:
                if created:
                    stock.delete()
                return None, "無効な証券コード、またはデータの取得に失敗しました。"
            stock.name = normalized_code
        else:
            stock.name = info.get('longName') or info.get('shortName') or normalized_code
    except Exception as e:
        # Sometimes ticker.info fails, but history works
        hist = ticker.history(period="1mo")
        if hist.empty:
            if created:
                stock.delete()
            return None, f"データ取得エラー: {str(e)}"
        stock.name = normalized_code

    stock.save()

    # Get 5 years of monthly history
    hist = ticker.history(period="5y", interval="1mo")

    if hist.empty:
        return None, "株価データを取得できませんでした。"

    # Clear old data if refreshing
    stock.monthly_data.all().delete()

    objs = []
    for index, row in hist.iterrows():
        date = index.date()
        dividend = row.get('Dividends', 0)
        closing_price = row.get('Close', 0)

        if closing_price > 0:
            dividend_yield = (dividend / closing_price) * 100
        else:
            dividend_yield = 0

        objs.append(MonthlyData(
            stock=stock,
            date=date,
            dividend=dividend,
            closing_price=closing_price,
            dividend_yield=dividend_yield
        ))

    MonthlyData.objects.bulk_create(objs)
    # Re-save to update last_updated
    stock.save()

    return stock, None
