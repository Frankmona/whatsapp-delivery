-- =========================================================================
-- FM XPRESS: Fix Critical Security Issue (Enable Row-Level Security / RLS)
-- Project: drsvzbrculuyavaqboku (FM XPRESS)
-- Run this script in your Supabase SQL Editor:
-- https://supabase.com/dashboard/project/drsvzbrculuyavaqboku/sql/new
-- =========================================================================

-- 1. Enable Row Level Security (RLS) on all public tables
-- This immediately resolves the 'rls_disabled_in_public' vulnerability in Supabase Security Advisor!
ALTER TABLE public.orders ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.riders ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS public.admin_users ENABLE ROW LEVEL SECURITY;

-- 2. Drop any previous open or insecure policies
DROP POLICY IF EXISTS "Allow service role full access to admin_users" ON public.admin_users;
DROP POLICY IF EXISTS "Allow service_role full access to orders" ON public.orders;
DROP POLICY IF EXISTS "Allow service_role full access to riders" ON public.riders;
DROP POLICY IF EXISTS "Allow service_role full access to admin_users" ON public.admin_users;
DROP POLICY IF EXISTS "Allow public access to orders" ON public.orders;
DROP POLICY IF EXISTS "Allow public access to riders" ON public.riders;

-- 3. Explicitly grant full access ONLY to the backend service_role
-- In Supabase, the backend using the service_role key has full administrative rights.
-- Public anonymous users (anon key) will have 0 direct access.
CREATE POLICY "Allow service_role full access to orders"
    ON public.orders
    FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true);

CREATE POLICY "Allow service_role full access to riders"
    ON public.riders
    FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true);

CREATE POLICY "Allow service_role full access to admin_users"
    ON public.admin_users
    FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true);

-- 4. Explicitly revoke public/anon access to prevent scraping or tampering
REVOKE ALL ON TABLE public.orders FROM anon;
REVOKE ALL ON TABLE public.riders FROM anon;
REVOKE ALL ON TABLE public.admin_users FROM anon;

-- Verification check: run this query to verify all tables show rowsecurity = true
SELECT tablename, rowsecurity 
FROM pg_tables 
WHERE schemaname = 'public' 
AND tablename IN ('orders', 'riders', 'admin_users');
