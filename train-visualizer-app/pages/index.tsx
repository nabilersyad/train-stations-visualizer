// pages/index.tsx
import { useEffect, useState } from 'react';
import { supabase } from '../utils/supabaseClient';

import Map from '../components/Map';


interface Station {
    name: string; // Name of the station
    station_code: string; // Alphanumeric code for the station as provided by operator or government
    service_provider_name: string; // Name of the service provider of the station
    latitude: number; // Latitude coordinate
    longitude: number; // Longitude coordinate
    route_id: string; // An Alphanumeric identifier for the route or train line the station is associated with
    route_name: string; // Name of the route or train line the station is associated with
    line_number: string; // Number of the that identifies the route train line the station is associated with
    line_colour: string; // Colour of the route train line the station is associated with
    colour_hex_code: string; // Hex code for the line color
    region: string; // Region where the station is located
    odonym: string; // Name or type of the road associated with the station
    namesake: string; // Namesake of the station
    opened: string; // Date or year the station was opened
    station_id: number; // Unique identifier for the station (bigint)
  }
  

const Home = () => {
  const [stations, setStations] = useState<Station[]>([]);
  const [isochrones, setIsochrones] = useState<any[]>([]);

  useEffect(() => {
    const fetchStations = async () => {
      const { data, error } = await supabase
        .from<Station>('stations')
        .select('*');
      if (error) console.log('Error fetching stations:', error);
      else setStations(data || []);
    };

    fetchStations();
  }, []);

  // Add the isochrone fetching logic here

  return (
    <div>
      <Map stations={stations} isochrones={isochrones} />
    </div>
  );
};

export default Home;
