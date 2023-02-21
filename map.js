import React from 'react';
import GoogleMapReact from 'google-map-react';
import data from './results.json';

const handleApiLoaded = (map, maps) => {
    // Total number of results is 410537, set to 1 for fast loading when editing
    for(let i=0; i < 410537; i+=2){
        const probability = parseFloat(data[i]['2014_fire_prob']);
        const latitude = parseFloat(data[i]['Latitude']);
        const longitude = parseFloat(data[i]['Longitude']);
        const rectangleCoords = [
            { lat: latitude + 0.00904372, lng: longitude + (1.0/(111.320*Math.cos(latitude*(Math.PI/180)))) },
            { lat: latitude + 0.00904372, lng: longitude - (1.0/(111.320*Math.cos(latitude*(Math.PI/180)))) },
            { lat: latitude - 0.00904372, lng: longitude - (1.0/(111.320*Math.cos(latitude*(Math.PI/180)))) },
            { lat: latitude - 0.00904372, lng: longitude + (1.0/(111.320*Math.cos(latitude*(Math.PI/180)))) },
            { lat: latitude + 0.00904372, lng: longitude + (1.0/(111.320*Math.cos(latitude*(Math.PI/180)))) }
        ];
        if( probability > 0.04 ){
            var rectangle = new maps.Polygon({
                paths: rectangleCoords,
                strokeColor: "#FF0000",
                strokeOpacity: 0,
                strokeWeight: 0,
                fillColor: "#FF0000",
                fillOpacity: 0.35
            });
            rectangle.setMap(map);
        }
        else if( (0.04 >= probability) && (probability > 0.02) ){
            var rectangle = new maps.Polygon({
                paths: rectangleCoords,
                strokeColor: "#FF0000",
                strokeOpacity: 0,
                strokeWeight: 0,
                fillColor: "#FF3800",
                fillOpacity: 0.35
            });
            rectangle.setMap(map);
        }
        else if( (0.02 >= probability) && (probability > 0.008) ){
            var rectangle = new maps.Polygon({
                paths: rectangleCoords,
                strokeColor: "#FF0000",
                strokeOpacity: 0,
                strokeWeight: 0,
                fillColor: "#FF6500",
                fillOpacity: 0.35
            });
            rectangle.setMap(map);
        }
        else if( (0.008 >= probability) && (probability > 0.006) ){
            var rectangle = new maps.Polygon({
                paths: rectangleCoords,
                strokeColor: "#FF0000",
                strokeOpacity: 0,
                strokeWeight: 0,
                fillColor: "#FF8700",
                fillOpacity: 0.35
            });
            rectangle.setMap(map);
        }
        else if( (0.006 >= probability) && (probability > 0.004) ){
            var rectangle = new maps.Polygon({
                paths: rectangleCoords,
                strokeColor: "#FF0000",
                strokeOpacity: 0,
                strokeWeight: 0,
                fillColor: "#FFa900",
                fillOpacity: 0.35
            });
            rectangle.setMap(map);
        }
        else if( (0.004 >= probability) && (probability > 0.002) ){
            var rectangle = new maps.Polygon({
                paths: rectangleCoords,
                strokeColor: "#FF0000",
                strokeOpacity: 0,
                strokeWeight: 0,
                fillColor: "#FFec00",
                fillOpacity: 0.35
            });
            rectangle.setMap(map);
        }
        else{
            var rectangle = new maps.Polygon({
                paths: rectangleCoords,
                strokeColor: "#FF0000",
                strokeOpacity: 0,
                strokeWeight: 0,
                fillColor: "#ADFF00",
                fillOpacity: 0.35
            });
            rectangle.setMap(map);
        }
        // var rectangle = new maps.Polygon({
        //     paths: rectangleCoords,
        //     strokeColor: "#FF0000",
        //     strokeOpacity: 0,
        //     strokeWeight: 0,
        //     fillColor: "#FF0000",
        //     fillOpacity: 0.35
        // });
        // rectangle.setMap(map);
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