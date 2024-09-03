// In a separate file (e.g., supabaseClient.ts)
import { createClient } from "@supabase/supabase-js";

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL  || ''; // Replace with your Supabase URL
const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY  || ''; // Replace with your Supabase public key

export const supabase = createClient(supabaseUrl, supabaseKey);

