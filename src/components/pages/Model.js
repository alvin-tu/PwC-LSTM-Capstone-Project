import React, { useState } from 'react'
import '../../App.css'
import Maps from './Maps.js';
import data from './results.json';

const maps = [
  {
    name: 'Prediction Year',
    lat: 0,
    lng: 0,
  },
  {
    name: 'California 2014',
    lat: 34.079036112228565,
    lng: -118.11952452923926,
    time: '2014',
  },
  {
    name: 'California 2015',
    lat: 34.079036112228565,
    lng: -118.11952452923926,
    time: '2015',
  },
  {
    name: 'California 2016',
    lat: 34.079036112228565,
    lng: -118.11952452923926,
    time: '2016',
  },
  {
    name: 'California 2017',
    lat: 34.079036112228565,
    lng: -118.11952452923926,
    time: '2017',
  },
];

export default function Model() {
  const [selectedMap, setSelectedMap] = useState(maps[0].name);

  const handleChange = (event) => {
    setSelectedMap(event.target.value);
  };

  return (
    <div>
      <h1 className="model">Model Dashboard</h1>
      <h1 style={{fontSize:'90px', alignItems: 'center'}}>Select a Year</h1>
      <div style={{marginLeft: '555px', marginBottom: '10px'}}>
        <select value={selectedMap} onChange={handleChange}>
          {maps.map((map) => (
            <option key={map.name} value={map.name}>
              {map.name}
            </option>
          ))}
        </select>
      </div>
      {maps
        .filter((map) => map.name === selectedMap)
        .map((map) => (
          <Maps
            key={map.name}
            lat={map.lat}
            lng={map.lng}
            year={map.time}
            data={data}
          />
        ))}
    </div>
  );
}
