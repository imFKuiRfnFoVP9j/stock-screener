# Fab Analytics Platform – 설계 요약 (Codex용)

## 1. 목표
- ET / EDS(HOT·COLD) / METRO 데이터 수천 item을
- 자유롭게 테이블·scatter·correlation으로 탐색
- lot / wafer / condition 필터에 즉시 반응
- 향후 **MET → ET 예측(ML)**까지 확장 가능

## 2. 핵심 원칙 (절대 변경 금지)
1. 저장 데이터는 항상 long format
2. wide(pivot)는 저장하지 않는다
3. scatter / correlation은 pivot 없이 SQL JOIN
4. pivot은 “표현용(테이블/ML)”에서만, 최소 item
5. Parquet = 캐시 / SQL = 질의 기준
6. Frontend는 SQL을 모른다 (FastAPI 경유)

## 3. 전체 아키텍처

```
[ Company Query ]
        ↓
[ Polars Transform / Normalize ]
        ↓
[ Parquet (long, cache) ]
        ↓
[ SQL DB (SQLite → PostgreSQL) ]
        ↓
[ FastAPI ]
        ↓
[ React + AG Grid + Chart ]
```

## 4. 데이터 모델 (Single Source of Truth)

Table: fact_measurement

```
lot_id      TEXT
wafer_no    INTEGER
source      TEXT        -- 'ET' | 'EDS' | 'METRO'
condition   TEXT        -- 'HOT' | 'COLD' | NULL
item_id     TEXT
value       DOUBLE
(track_time, ppid, tool_id optional)
```

필수 인덱스

```
(lot_id, wafer_no, source, item_id, condition)
```

## 5. Ingest / Transform 규칙 (Polars)
- ET / EDS / METRO는 같은 스키마로 통합
- source, condition 컬럼 추가
- item_id 표준화 (CSV mapping)
- 단위 변환 수행
- pivot 금지

결과:

```
measurement_long.parquet
```

## 6. SQL 사용 규칙

❌ 금지
- wide 테이블 저장
- SELECT *
- 전체 item pivot

✅ 허용
- WHERE로 lot/wafer/condition 필터
- item 2~N개 JOIN
- subset pivot (테이블 표시용)

## 7. Scatter / Correlation 패턴 (pivot ❌)

```sql
SELECT
  a.value AS x,
  b.value AS y
FROM fact_measurement a
JOIN fact_measurement b
  ON a.lot_id=b.lot_id AND a.wafer_no=b.wafer_no
WHERE
  a.source=:x_source AND a.item_id=:x_item
  AND b.source=:y_source AND b.item_id=:y_item
  AND a.lot_id=:lot
  AND (:condition IS NULL OR a.condition=:condition);
```

- item 수가 1,000개여도 코드 변경 없음
- 거의 모든 item 조합 scatter 가능

## 8. 테이블 표시 패턴 (subset pivot)
- 대표 item 10~50개만 컬럼으로 표시
- SQL CASE WHEN pivot 또는 Polars pivot

```sql
MAX(CASE WHEN item_id='Vth' THEN value END) AS Vth
```

## 9. FastAPI 역할 (필수)
- Frontend ↔ DB 사이 유일한 창구
- SQL 직접 노출 ❌
- 쿼리 패턴 표준화
- DB 교체(SQLite → PostgreSQL) 대응

주요 API

- GET /api/scatter
- GET /api/table
- GET /api/items
- GET /api/lots
- (확장) POST /api/predict

## 10. Frontend 선택
- React + AG Grid + ECharts/Plotly (권장)
- 역할:
  - 상태 관리 (lot / wafer / item / condition)
  - FastAPI 호출
  - 테이블·차트 렌더링
  - 계산/가공 ❌ (전부 Backend/SQL)

## 11. Parquet의 역할
- 중간 캐시
- 재현성
- SQL 재적재
- DuckDB/ML 실험용

❗ Parquet은 “결과 파일”이 아니다

## 12. ML 확장 (MET → ET 예측)
- Feature: METRO + EDS
- Label: ET (Vth, Ion 등)
- 학습 직전에만 pivot
- SQL → Polars → XGBoost / LightGBM

```
long (SQL) → ML용 wide (임시) → 모델
```

## 13. 권장 파일 구조 (요약)

```
ingest/        # 회사 쿼리
transform/     # Polars 정규화
data/parquet/  # long parquet
db/            # SQL 적재
api/           # FastAPI
frontend/      # React + AG Grid
ml/            # ML 실험/예측
```

## 14. 핵심 문장 (이것만 기억해도 됨)

Parquet은 저장,
SQL은 질의,
Pivot은 표현,
FastAPI는 두뇌,
React는 인터랙션.
