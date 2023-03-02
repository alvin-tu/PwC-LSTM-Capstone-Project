import React from 'react';
import GoogleMapReact from 'google-map-react';
// import data from './results.json';
import data04 from './2014_predictions/reduced_coordinates_04.json';
import data02 from './2014_predictions/reduced_coordinates_02.json';
import data008 from './2014_predictions/reduced_coordinates_008.json';
import data006 from './2014_predictions/reduced_coordinates_006.json';
import data004 from './2014_predictions/reduced_coordinates_004.json';
import data002 from './2014_predictions/reduced_coordinates_002.json';
import data00 from './2014_predictions/reduced_coordinates_00.json';


const handleApiLoaded = (map, maps) => {
    for(let i=0; i < data04.length; i++){
        let polygonCoords = []
        for(let j = 0; j < data04[i].length; j++){
            polygonCoords.push({ lat: data04[i][j][1], lng: data04[i][j][0]})
            
        }
        var rectangle = new maps.Polygon({
            paths: polygonCoords,
            strokeColor: "#FF0000",
            strokeOpacity: 0.5,
            strokeWeight: 1,
            fillColor: "#FF0000",
            fillOpacity: 0.35
        });
        rectangle.setMap(map);
    }  
    for(let i=0; i < data02.length; i++){
        let polygonCoords = []
        for(let j = 0; j < data02[i].length; j++){
            polygonCoords.push({ lat: data02[i][j][1], lng: data02[i][j][0]})
            
        }
        var rectangle = new maps.Polygon({
            paths: polygonCoords,
            strokeColor: "#ff8000",
            strokeOpacity: 0.5,
            strokeWeight: 1,
            fillColor: "#ff8000",
            fillOpacity: 0.35
        });
        rectangle.setMap(map);
    }   
    for(let i=0; i < data008.length; i++){
        let polygonCoords = []
        for(let j = 0; j < data008[i].length; j++){
            polygonCoords.push({ lat: data008[i][j][1], lng: data008[i][j][0]})
            
        }
        var rectangle = new maps.Polygon({
            paths: polygonCoords,
            strokeColor: "#ffff00",
            strokeOpacity: 0.5,
            strokeWeight: 1,
            fillColor: "#ffff00",
            fillOpacity: 0.35
        });
        rectangle.setMap(map);
    }  
    for(let i=0; i < data006.length; i++){
        let polygonCoords = []
        for(let j = 0; j < data006[i].length; j++){
            polygonCoords.push({ lat: data006[i][j][1], lng: data006[i][j][0]})
            
        }
        var rectangle = new maps.Polygon({
            paths: polygonCoords,
            strokeColor: "#40ff00",
            strokeOpacity: 0.5,
            strokeWeight: 1,
            fillColor: "#40ff00",
            fillOpacity: 0.35
        });
        rectangle.setMap(map);
    } 
    for(let i=0; i < data004.length; i++){
        let polygonCoords = []
        for(let j = 0; j < data004[i].length; j++){
            polygonCoords.push({ lat: data004[i][j][1], lng: data004[i][j][0]})
            
        }
        var rectangle = new maps.Polygon({
            paths: polygonCoords,
            strokeColor: "#00ffff",
            strokeOpacity: 0.5,
            strokeWeight: 1,
            fillColor: "#00ffff",
            fillOpacity: 0.35
        });
        rectangle.setMap(map);
    }  
    for(let i=0; i < data002.length; i++){
        let polygonCoords = []
        for(let j = 0; j < data002[i].length; j++){
            polygonCoords.push({ lat: data002[i][j][1], lng: data002[i][j][0]})
            
        }
        var rectangle = new maps.Polygon({
            paths: polygonCoords,
            strokeColor: "#0000ff",
            strokeOpacity: 0.5,
            strokeWeight: 1,
            fillColor: "#0000ff",
            fillOpacity: 0.35
        });
        rectangle.setMap(map);
    }   
    for(let i=0; i < data00.length; i++){
        let polygonCoords = []
        for(let j = 0; j < data00[i].length; j++){
            polygonCoords.push({ lat: data00[i][j][1], lng: data00[i][j][0]})
            
        }
        var rectangle = new maps.Polygon({
            paths: polygonCoords,
            strokeColor: "#bf00ff",
            strokeOpacity: 0.5,
            strokeWeight: 1,
            fillColor: "#bf00ff",
            fillOpacity: 0.35
        });
        rectangle.setMap(map);
    }   
}

export default function Map(){
    const defaultProps = {
        center:{
            lat: 38.323907,
            lng: -119.109291
        },
        zoom: 6
    };
    return(
        <div style={{height:'100%', width:'100%'}}>
            <GoogleMapReact
                style = {{width: "100%", height: "100%"}}
                bootstrapURLKeys={{key: "AIzaSyDnI1LPymxoYhoa-qVAV2gBIKTm1gpIHVA"}}
                defaultCenter={defaultProps.center}
                defaultZoom={defaultProps.zoom}
                yesIWantToUseGoogleMapApiInternals
                onGoogleApiLoaded={({ map, maps }) => handleApiLoaded(map, maps)}
            >
            </GoogleMapReact>
        </div>
    );
}