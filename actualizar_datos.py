#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
actualizar_datos.py — Descarga ~3 años OHLCV diario (Yahoo chart v8) + fundamentales
(quoteSummary v10) para las 25 empresas del White House AI Stack y genera
datos_reales.json con el esquema EXACTO que espera index.html.

Uso:  python actualizar_datos.py [--salida datos_reales.json]
Requisitos: solo librería estándar (urllib, json).

NOTA CORS: la página NO llama a Yahoo directamente porque el navegador bloquea la
respuesta (Yahoo no envía Access-Control-Allow-Origin). Este script corre del lado
escritorio/servidor, sin esa restricción, y produce el JSON que se carga con el botón
"Cargar datos reales (JSON)" de la página (o automáticamente vía GitHub Actions).
"""
import json, time, argparse, urllib.request, urllib.error
from datetime import datetime, timezone

TICKERS = ["VST","CEG","OKLO","EOSE","GEV","NVDA","AMD","TSM","MU","ARM",
           "NBIS","IREN","CRWV","APLD","CIFR","MSFT","GOOGL","META","AMZN",
           "ORCL","PLTR","TSLA","NOW","SNOW","CRM"]
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"}
CHART = "https://query1.finance.yahoo.com/v8/finance/chart/{tk}?range=3y&interval=1d&events=div,splits"
QSUM  = ("https://query2.finance.yahoo.com/v10/finance/quoteSummary/{tk}?modules="
         "incomeStatementHistory,balanceSheetHistory,cashflowStatementHistory,"
         "defaultKeyStatistics,financialData")

def fetch(url, intentos=3):
    for i in range(intentos):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read().decode("utf-8"))
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as e:
            print(f"  reintento {i+1}: {e}"); time.sleep(2*(i+1))
    return None

def ohlcv(tk):
    j = fetch(CHART.format(tk=tk))
    if not j or not j.get("chart", {}).get("result"): return None
    res = j["chart"]["result"][0]; ts = res.get("timestamp", [])
    q = res["indicators"]["quote"][0]
    dates, o, h, l, c, v = [], [], [], [], [], []
    for i, t in enumerate(ts):
        if q["close"][i] is None: continue
        dates.append(datetime.fromtimestamp(t, tz=timezone.utc).strftime("%Y-%m-%d"))
        o.append(round(q["open"][i], 4)); h.append(round(q["high"][i], 4))
        l.append(round(q["low"][i], 4));  c.append(round(q["close"][i], 4))
        v.append(int(q["volume"][i] or 0))
    return {"dates": dates, "open": o, "high": h, "low": l, "close": c, "volume": v}

def _val(node, key):
    try:
        x = node[key]; return x.get("raw") if isinstance(x, dict) else x
    except Exception:
        return None

def fundamentals(tk):
    j = fetch(QSUM.format(tk=tk))
    if not j or not j.get("quoteSummary", {}).get("result"): return None
    r = j["quoteSummary"]["result"][0]; M = 1e6
    try:
        inc = r["incomeStatementHistory"]["incomeStatementHistory"][0]
        bs  = r["balanceSheetHistory"]["balanceSheetStatements"][0]
        cf  = r["cashflowStatementHistory"]["cashflowStatements"][0]
        ks  = r.get("defaultKeyStatistics", {}); fd = r.get("financialData", {})
        def mm(node, k):
            x = _val(node, k); return round(x / M, 2) if x is not None else None
        return {k: v for k, v in {
            "rev": mm(inc, "totalRevenue"), "ni": mm(inc, "netIncome"), "ebitda": mm(fd, "ebitda"),
            "ta": mm(bs, "totalAssets"), "eq": mm(bs, "totalStockholderEquity"),
            "debt": mm(bs, "longTermDebt"), "cash": mm(bs, "cash"),
            "ca": mm(bs, "totalCurrentAssets"), "cl": mm(bs, "totalCurrentLiabilities"),
            "cfo": mm(cf, "totalCashFromOperatingActivities"),
            "sh": round((_val(ks, "sharesOutstanding") or 0) / M, 2) or None
        }.items() if v is not None}
    except Exception as e:
        print(f"  fundamentales {tk} no disponibles: {e}"); return None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--salida", default="datos_reales.json")
    args = ap.parse_args()
    salida = {"updated": datetime.now().strftime("%Y-%m-%d"),
              "source": "Yahoo Finance chart v8 + quoteSummary v10", "tickers": {}}
    for tk in TICKERS:
        print(f"Descargando {tk} ...")
        px = ohlcv(tk)
        if px is None:
            print(f"  ⚠ ERROR OHLCV {tk}; se omite.")
            continue
        entry = dict(px)
        fu = fundamentals(tk)
        if fu: entry["fund"] = fu
        salida["tickers"][tk] = entry
        time.sleep(1.2)
    faltan = [t for t in TICKERS if t not in salida["tickers"]]
    if faltan:
        print(f"⚠ Faltaron: {faltan}. La página validará el esquema y avisará.")
    with open(args.salida, "w", encoding="utf-8") as f:
        json.dump(salida, f, ensure_ascii=False)
    print(f"✔ Generado {args.salida} con {len(salida['tickers'])}/25 tickers.")

if __name__ == "__main__":
    main()
