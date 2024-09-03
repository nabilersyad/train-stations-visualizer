// components/Map.tsx
import { FC } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Polygon } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

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
  


interface IsochroneFeature {
  type: string;
  geometry: {
    type: string;
    coordinates: number[][][];
  };
}

interface IsochroneResponse {
  features: IsochroneFeature[];
}

interface MapProps {
  stations: Station[];
  isochrones: IsochroneResponse[];
}

const Map: FC<MapProps> = ({ stations, isochrones }) => {
  return (
    <MapContainer center={[51.505, -0.09]} zoom={13} style={{ height: '100vh', width: '100%' }}>
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      />
      {stations.map((station) => (
        <Marker key={station.station_id} position={[station.latitude, station.longitude]}>
          <Popup>{station.name}</Popup>
        </Marker>
      ))}
      {isochrones.map((iso, idx) => (
        iso.features.map((feature, idx2) => (
          <Polygon key={`${idx}-${idx2}`} positions={feature.geometry.coordinates[0].map(coord => [coord[1], coord[0]])} />
        ))
      ))}
    </MapContainer>
  );
};

export default Map;
