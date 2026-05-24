import { useEffect, useRef } from "react";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import "./DeliveryMap.css";

function DeliveryMap({ tracking }) {
  const mapRef = useRef(null);
  const mapInstance = useRef(null);

  useEffect(() => {
    if (!tracking || !mapRef.current) return;

    const customer = tracking.customer;
    const hub = tracking.hub;
    const current = tracking.current_position;

    if (mapInstance.current) {
      mapInstance.current.remove();
      mapInstance.current = null;
    }

    const map = L.map(mapRef.current, { zoomAnimation: false, fadeAnimation: false }).setView([current.lat, current.lng], 13);
    mapInstance.current = map;

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution: "&copy; OpenStreetMap",
    }).addTo(map);

    const hubIcon = L.divIcon({
      className: "map-marker hub",
      html: "📦",
      iconSize: [28, 28],
    });
    const riderIcon = L.divIcon({
      className: "map-marker rider",
      html: "🛵",
      iconSize: [28, 28],
    });
    const homeIcon = L.divIcon({
      className: "map-marker home",
      html: "🏠",
      iconSize: [28, 28],
    });

    L.marker([hub.lat, hub.lng], { icon: hubIcon }).addTo(map).bindPopup("ShopSphere Hub");
    L.marker([current.lat, current.lng], { icon: riderIcon })
      .addTo(map)
      .bindPopup("Delivery in progress");
    L.marker([customer.lat, customer.lng], { icon: homeIcon })
      .addTo(map)
      .bindPopup("Delivery address");

    const route = [
      [hub.lat, hub.lng],
      [current.lat, current.lng],
      [customer.lat, customer.lng],
    ];
    L.polyline(route, { color: "#667eea", weight: 4, dashArray: "8 8" }).addTo(map);
    map.fitBounds(route, { padding: [40, 40] });

    return () => {
      if (mapInstance.current) {
        try {
          mapInstance.current.stop();
          mapInstance.current.remove();
        } catch (_) {}
        mapInstance.current = null;
      }
    };
  }, [tracking]);

  if (!tracking) {
    return <div className="map-placeholder">Map loading...</div>;
  }

  return <div ref={mapRef} className="delivery-map" />;
}

export default DeliveryMap;
