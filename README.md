### Python script to create MapServer .map file from a WMS GetCapabilities document

Example URLs to test that the generated MapServer .map file does indeed return WMS responses:
* [MapServer Map request](http://localhost:8080/cgi-bin/mapserv?map=/vagrant/maps/test-01.map&layer=LC.LandCoverSurfaces&mode=map)
* [MapServer WMS 1.1.0 GetCapabilities request](http://localhost:8080/cgi-bin/mapserv?map=/vagrant/maps/test-01.map&SERVICE=WMS&VERSION=1.1.1&REQUEST=GetCapabilities)
* [MapServer WMS 1.1.1 GetMap request (full GB extent)](http://localhost:8080/cgi-bin/mapserv?map=/vagrant/maps/test-01.map&SERVICE=WMS&VERSION=1.1.1&REQUEST=GetMap&layers=LC.LandCoverSurfaces&styles=&srs=epsg:27700&bbox=0,0,700000,1300000&format=image/png&width=350&height=650)
* [MapServer WMS 1.1.1 GetMap request (OS SD 100 km tile)](http://localhost:8080/cgi-bin/mapserv?map=/vagrant/maps/test-01.map&SERVICE=WMS&VERSION=1.1.10&REQUEST=GetMap&layers=LC.LandCoverSurfaces&styles=&srs=epsg:27700&bbox=300000,40000,400000,500000&format=image/png&width=350&height=350)
* [MapServer WMS 1.3.0 GetCapabilities request](http://localhost:8080/cgi-bin/mapserv?map=/vagrant/maps/test-01.map&SERVICE=WMS&VERSION=1.3.0&REQUEST=GetCapabilities)
* [MapServer WMS 1.3.0 GetMap request (full GB extent)](http://localhost:8080/cgi-bin/mapserv?map=/vagrant/maps/test-01.map&SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&layers=LC.LandCoverSurfaces&styles=&crs=epsg:27700&bbox=0,0,700000,1300000&format=image/png&width=350&height=650)
* [MapServer WMS 1.3.0 GetMap request (OS SD 100 km tile)](http://localhost:8080/cgi-bin/mapserv?map=/vagrant/maps/test-01.map&SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&layers=LC.LandCoverSurfaces&styles=&crs=epsg:27700&bbox=300000,40000,400000,500000&format=image/png&width=350&height=350)


