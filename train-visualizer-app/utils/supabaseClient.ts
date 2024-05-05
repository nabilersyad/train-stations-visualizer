// In a separate file (e.g., supabaseClient.ts)
import { createClient } from "@supabase/supabase-js";

const supabaseUrl = "YOUR_SUPABASE_URL"; // Replace with your Supabase URL
const supabaseKey = "YOUR_SUPABASE_PUBLIC_KEY"; // Replace with your Supabase public key

const supabase = createClient(supabaseUrl, supabaseKey);

export async function getTrainStations(): Promise<TrainStation[]> {
  const { data, error } = await supabase
    .from("YOUR_TABLE_NAME") // Replace with your actual table name
    .select("*");

  if (error) {
    console.error("Error fetching train stations:", error);
    return []; // Handle error gracefully (e.g., display error message)
  }

  return data;
}

// Interface for your train station data structure
interface TrainStation {
  id: number;
  name: string;
  latitude: number;
  longitude: number;
  // ... other station properties (if applicable)
}