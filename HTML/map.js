function initMap() {
    const map = new google.maps.Map(document.getElementById("map"), {
      zoom: 11,
      center: { lat: 36.323907, lng: -119.109291 },
      mapTypeId: "roadmap",
    });
    const bounds = new google.maps.LatLngBounds(
      new google.maps.LatLng(32.417832, -124.482003),
      new google.maps.LatLng(41.898517, -114.131211)
    );
  
    /**
     * Comment out one of the two pairs below. The first pair has
     * a purple background showing CA, while the other doesn't
     */

    let image_actual = "fire_output_actual.png";
    let image_prediction= "fire_output_predicted.png";

    // let image_actual = "fire_output_actual_no_purple.png";
    // let image_prediction= "fire_output_predicted_no_purple.png";

    /**
     * The Overlay object contains the image,
     * the bounds of the image, and a reference to the map.
     */
    class Overlay extends google.maps.OverlayView {
      bounds;
      image;
      div;
      constructor(bounds, image) {
        super();
        this.bounds = bounds;
        this.image = image;
      }
      /**
       * onAdd is called when the map's panes are ready and the overlay has been
       * added to the map.
       */
      onAdd() {
        this.div = document.createElement("div");
        this.div.style.borderStyle = "none";
        this.div.style.borderWidth = "0px";
        this.div.style.position = "absolute";
  
        // Create the img element and attach it to the div.
        const img = document.createElement("img");
  
        img.src = this.image;
        img.style.width = "100%";
        img.style.height = "100%";
        img.style.position = "absolute";
        img.style.opacity = "50%";
        this.div.appendChild(img);
  
        // Add the element to the "overlayLayer" pane.
        const panes = this.getPanes();
  
        panes.overlayLayer.appendChild(this.div);
      }

      draw() {
        // Use the south-west and north-east
        // coordinates of the overlay to get correct position and size.
        // Retrieve the projection from the overlay.
        const overlayProjection = this.getProjection();
        // Retrieve the south-west and north-east coordinates of this overlay
        // in LatLngs and convert them to pixel coordinates.
        // Use these coordinates to resize the div.
        const sw = overlayProjection.fromLatLngToDivPixel(
          this.bounds.getSouthWest()
        );
        const ne = overlayProjection.fromLatLngToDivPixel(
          this.bounds.getNorthEast()
        );
  
        // Resize the image's div to fit the indicated dimensions.
        if (this.div) {
          this.div.style.left = sw.x + "px";
          this.div.style.top = ne.y + "px";
          this.div.style.width = ne.x - sw.x + "px";
          this.div.style.height = sw.y - ne.y + "px";
        }
      }
    
      /**
       *  Set the visibility to 'hidden' or 'visible'.
       */
      hide() {
        if (this.div) {
          this.div.style.visibility = "hidden";
        }
      }
      show() {
        if (this.div) {
          this.div.style.visibility = "visible";
        }
      }
      toggle() {
        if (this.div) {
          if (this.div.style.visibility === "hidden") {
            this.show();
          } else {
            this.hide();
          }
        }
      }
      toggleDOM(map) {
        if (this.getMap()) {
          this.setMap(null);
        } else {
          this.setMap(map);
        }
      }
    }
  
    const overlay_actual = new Overlay(bounds, image_actual);
    const overlay_prediction = new Overlay(bounds, image_prediction);
  
    overlay_actual.setMap(map);
    overlay_prediction.setMap(map);
  
    const toggleActualButton = document.createElement("button");
  
    toggleActualButton.textContent = "Toggle Expected";
    toggleActualButton.classList.add("custom-map-control-button");
  
    toggleActualButton.addEventListener("click", () => {
      overlay_actual.toggle();
    });

    const togglePredictButton = document.createElement("button");
    togglePredictButton.textContent = "Toggle Prediction";
    togglePredictButton.classList.add("custom-map-control-button");
    togglePredictButton.addEventListener("click", () => {
      overlay_prediction.toggle();
    });

    map.controls[google.maps.ControlPosition.TOP_RIGHT].push(togglePredictButton);
    map.controls[google.maps.ControlPosition.TOP_RIGHT].push(toggleActualButton);
  }
  
  window.initMap = initMap;
