import React, { useRef, useEffect } from 'react';
import data from './results.json';
import html2canvas from 'html2canvas';

const mapStyles = [
    {
      featureType: "all",
      elementType: "labels.text.fill",
      stylers: [
        { saturation: -100 },
        { lightness: 50 }
      ]
    },
    {
      featureType: "all",
      elementType: "labels.icon",
      stylers: [
        { saturation: -100 },
        { lightness: 50 }
      ]
    },
    {
      featureType: "administrative",
      elementType: "geometry.fill",
      stylers: [
        { saturation: -100 },
        { lightness: 50 }
      ]
    },
    {
      featureType: "administrative",
      elementType: "geometry.stroke",
      stylers: [
        { saturation: -100 },
        { lightness: 50 }
      ]
    },
    {
      featureType: "landscape",
      elementType: "geometry",
      stylers: [
        { saturation: -100 },
        { lightness: 50 }
      ]
    },
    {
      featureType: "poi",
      elementType: "geometry",
      stylers: [
        { saturation: -100 },
        { lightness: 50 }
      ]
    },
    {
      featureType: "road",
      elementType: "geometry",
      stylers: [
        { saturation: -100 },
        { lightness: 50 }
      ]
    },
    {
      featureType: "transit",
      elementType: "geometry",
      stylers: [
        { saturation: -100 },
        { lightness: 50 }
      ]
    },
    {
      featureType: "water",
      elementType: "geometry",
      stylers: [
        { saturation: -100 },
        { lightness: 50 }
      ]
    }
  ];

const Maps = ({ lat, lng, year }) => {
    const mapRef = useRef(null);

    useEffect(() => {
        const script = document.createElement('script');
        script.src = `https://maps.googleapis.com/maps/api/js?key={INPUT YOUR OWN KEY}`;
        script.async = true;
        script.onload = () => {
            const map = new window.google.maps.Map(mapRef.current, {
            center: { lat, lng },
            zoom: 6,
            styles: mapStyles
            });
        
        // Downsample the pixel data
        const downsampledData = downsample(data, 2); // Sample every nth pixel

        // Display each downsampled pixel as a square polygon on the map
        downsampledData.forEach((pixel) => {
            const polygon = new window.google.maps.Polygon({
            paths: [
                { lat: Number(pixel.Latitude) + 0.00904372, lng: Number(pixel.Longitude) + (1.0/(111.320*Math.cos(Number(pixel.Latitude)*(Math.PI/180)))) },
                { lat: Number(pixel.Latitude) + 0.00904372, lng: Number(pixel.Longitude) - (1.0/(111.320*Math.cos(Number(pixel.Latitude)*(Math.PI/180)))) },
                { lat: Number(pixel.Latitude) - 0.00904372, lng: Number(pixel.Longitude) - (1.0/(111.320*Math.cos(Number(pixel.Latitude)*(Math.PI/180)))) },
                { lat: Number(pixel.Latitude) - 0.00904372, lng: Number(pixel.Longitude) + (1.0/(111.320*Math.cos(Number(pixel.Latitude)*(Math.PI/180)))) },
                { lat: Number(pixel.Latitude) + 0.00904372, lng: Number(pixel.Longitude) + (1.0/(111.320*Math.cos(Number(pixel.Latitude)*(Math.PI/180)))) }
            ],
            strokeOpacity: 0,
            strokeWeight: 0,
            fillColor: getColor(pixel[`${year}_fire_prob`]),
            fillOpacity: 0.25,
            });
            polygon.setMap(map);
        });
    };
    document.body.appendChild(script);
  }, [lat, lng, year]);
  
  if (!lat || !lng) {
    return (
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
            <div
            style={{ height: '700px', width: '700px', border: '1.5px solid black',
            borderRadius: '10px', marginBottom: '20px'}}
            >
            <div style={{
                display: 'flex',
                color: 'black',
                fontSize: '5rem',
                fontWeight: 'bold',
                position: 'absolute',
                top: '1290px',
                left: '617px',
            }}>
                No Year Selected
            </div>
            </div>
            <Legend />
        </div>
        );
    }
    return (
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
            <div ref={mapRef} style={{ height: '700px', width: '700px', border: '1.5px solid black', borderRadius: '10px', marginBottom: '20px' }}></div>
                <Legend />
                <button onClick={saveMapImage}>Save Image</button>
        </div>
        );
    };

    function downsample(data, sampleRate) {
        // Sample every sampleRate-th pixel
        return data.filter((pixel, index) => index % sampleRate === 0);
    }

    function getColor(value) {
        // Determine the color based on the value of 2014_fire_prob
        if( value > 0.04 ){
            return "#FF0000";
        }
        else if( (0.04 >= value) && (value > 0.02) ){
            return "#FF6A00";
        }
        else if( (0.02 >= value) && (value > 0.008) ){
            return "#FFC400";
        }
        else if( (0.008 >= value) && (value > 0.006) ){
            return "#EAFF00";
        }
        else if( (0.006 >= value) && (value > 0.004) ){
            return "#66FF00";
        }
        else if( (0.004 >= value) && (value > 0.002) ){
            return "#00FFEA";
        }
        else {
            return "#0091FF";
        }
    }

    function Legend() {
        return (
            <div
              style={{
                top: '1250px',
                backgroundColor: 'white',
                padding: '10px',
                borderRadius: '5px',
                position: 'absolute',
                bottom: '10px',
                right: '250px',
              }}
            >
              <h3>Legend</h3>
                <div>
                    <span style={{ backgroundColor: '#FF0000', width: '20px', height: '20px', display: 'inline-block', marginRight: '5px' }} />
                    0.04 {"<"} Probability
                </div>
                <div>
                    <span style={{ backgroundColor: '#FF6A00', width: '20px', height: '20px', display: 'inline-block', marginRight: '5px' }} />
                    0.2 {"<"} Probability {"<="} 0.04
                </div>
                <div>
                    <span style={{ backgroundColor: '#FFC400', width: '20px', height: '20px', display: 'inline-block', marginRight: '5px' }} />
                    0.008 {"<"} Probability {"<="} 0.02
                </div>
                <div>
                    <span style={{ backgroundColor: '#EAFF00', width: '20px', height: '20px', display: 'inline-block', marginRight: '5px' }} />
                    0.006 {"<"} Probability {"<="} 0.008
                </div>
                <div>
                    <span style={{ backgroundColor: '#66FF00', width: '20px', height: '20px', display: 'inline-block', marginRight: '5px' }} />
                    0.004 {"<"} Probability {"<="} 0.006
                </div>
                <div>
                    <span style={{ backgroundColor: '#00FFEA', width: '20px', height: '20px', display: 'inline-block', marginRight: '5px' }} />
                    0.002 {"<"} Probability {"<="} 0.004
                </div>
                <div>
                    <span style={{ backgroundColor: '#0091FF', width: '20px', height: '20px', display: 'inline-block', marginRight: '5px' }} />
                    0.002 {">="} Probability
                </div>
            </div>
          );
    }

  export default Maps;
