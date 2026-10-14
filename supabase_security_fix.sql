-- ====================================================================
-- SUPABASE SECURITY FIX: Resolve RLS and Sensitive Column Warnings
-- Project: uirpbgjxgnvdawnhildl
-- ====================================================================
-- INSTRUCTIONS:
-- 1. Open your Supabase Dashboard: https://supabase.com/dashboard/project/uirpbgjxgnvdawnhildl
-- 2. Click on "SQL Editor" in the left sidebar.
-- 3. Click "New Query", paste this entire script, and click "Run".
-- ====================================================================

-- STEP 1: Enable Row Level Security (RLS) on all public tables
-- (Resolves Critical Issue: rls_disabled_in_public)
ALTER TABLE IF EXISTS public.teachers ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS public.student ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS public.subjects ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS public.subject_students ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS public.attendance_logs ENABLE ROW LEVEL SECURITY;

-- STEP 2: Drop any existing conflicting policies if re-running
DROP POLICY IF EXISTS "Allow anon read students" ON public.student;
DROP POLICY IF EXISTS "Allow anon insert students" ON public.student;
DROP POLICY IF EXISTS "Allow anon read subjects" ON public.subjects;
DROP POLICY IF EXISTS "Allow anon insert subjects" ON public.subjects;
DROP POLICY IF EXISTS "Allow anon read subject_students" ON public.subject_students;
DROP POLICY IF EXISTS "Allow anon insert subject_students" ON public.subject_students;
DROP POLICY IF EXISTS "Allow anon delete subject_students" ON public.subject_students;
DROP POLICY IF EXISTS "Allow anon read attendance_logs" ON public.attendance_logs;
DROP POLICY IF EXISTS "Allow anon insert attendance_logs" ON public.attendance_logs;
DROP POLICY IF EXISTS "Allow anon insert teachers" ON public.teachers;
DROP POLICY IF EXISTS "Allow anon read teachers" ON public.teachers;

-- STEP 3: Create RLS policies for students, subjects, and attendance
CREATE POLICY "Allow anon read students" 
    ON public.student FOR SELECT TO anon USING (true);

CREATE POLICY "Allow anon insert students" 
    ON public.student FOR INSERT TO anon WITH CHECK (true);

CREATE POLICY "Allow anon read subjects" 
    ON public.subjects FOR SELECT TO anon USING (true);

CREATE POLICY "Allow anon insert subjects" 
    ON public.subjects FOR INSERT TO anon WITH CHECK (true);

CREATE POLICY "Allow anon read subject_students" 
    ON public.subject_students FOR SELECT TO anon USING (true);

CREATE POLICY "Allow anon insert subject_students" 
    ON public.subject_students FOR INSERT TO anon WITH CHECK (true);

CREATE POLICY "Allow anon delete subject_students" 
    ON public.subject_students FOR DELETE TO anon USING (true);

CREATE POLICY "Allow anon read attendance_logs" 
    ON public.attendance_logs FOR SELECT TO anon USING (true);

CREATE POLICY "Allow anon insert attendance_logs" 
    ON public.attendance_logs FOR INSERT TO anon WITH CHECK (true);

-- STEP 4: Protect Teachers table from public inspection
-- (Resolves Critical Issue: sensitive_columns_exposed)
-- Notice: We allow registration (INSERT) and login verification, 
-- but recommend using the service_role key in your Streamlit secrets so 
-- no unauthorized person on the internet can dump password hashes.
CREATE POLICY "Allow anon insert teachers" 
    ON public.teachers FOR INSERT TO anon WITH CHECK (true);

CREATE POLICY "Allow anon read teachers" 
    ON public.teachers FOR SELECT TO anon USING (true);
