-- ==============================================================================
-- SnapClass: Update Attendance Timestamps to Indian Standard Time (IST)
--
-- How to run:
-- 1. Open your Supabase Dashboard: https://supabase.com/dashboard
-- 2. Select your project ("uirpbgjxgnvdawnhildl")
-- 3. Click on "SQL Editor" in the left sidebar
-- 4. Click "New query", paste this entire script, and click "Run" (or Ctrl+Enter)
-- ==============================================================================

-- STEP 1: Remove scratch test rows
DELETE FROM public.attendance_logs 
WHERE id IN (19, 26);

-- STEP 2: Update all existing attendance records to Indian Standard Time (IST)
-- This shifts existing UTC timestamps into Asia/Kolkata local time (+5 hours 30 minutes)
-- and updates the column to store local time so the Supabase Table Editor displays
-- the exact local classroom time directly (e.g. 21:58:42 for 09:58 PM).
ALTER TABLE public.attendance_logs 
    ALTER COLUMN timestamp TYPE timestamp without time zone 
    USING (timestamp AT TIME ZONE 'Asia/Kolkata');

-- STEP 3: Add UPDATE and DELETE policies for attendance_logs so you can manage them
DROP POLICY IF EXISTS "Allow anon update attendance_logs" ON public.attendance_logs;
CREATE POLICY "Allow anon update attendance_logs" 
    ON public.attendance_logs FOR UPDATE TO anon USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "Allow anon delete attendance_logs" ON public.attendance_logs;
CREATE POLICY "Allow anon delete attendance_logs" 
    ON public.attendance_logs FOR DELETE TO anon USING (true);

-- STEP 4: Verify the updated rows
SELECT id, timestamp, subject_id, student_id, is_present 
FROM public.attendance_logs 
ORDER BY id DESC 
LIMIT 10;
