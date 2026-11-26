-- 1. items 테이블 생성
CREATE TABLE IF NOT EXISTS public.items (
    id BIGSERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    category TEXT DEFAULT 'general',
    price NUMERIC(10, 2) DEFAULT 0.00,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. 테이블 컬럼 추가/변경 예시 (ALTER)
ALTER TABLE public.items
ADD COLUMN IF NOT EXISTS description TEXT;

-- 3. Row Level Security (RLS) 활성화 및 기본 정책
ALTER TABLE public.items ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow public read access"
ON public.items FOR SELECT
USING (true);