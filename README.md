# PI Client

## Client side

- Literally everything was me:tm:  -R
    - Specifically, the core structure of the code (both extraneous code like discord reports and the underlying base classes of the sensors. Also, two of the modes in the camera. Also, the client-sided data parsing from the server's websocket.)
- I helped -V
    - I did the other mode for the camera and wrote the original structure of the sensors before R refactored it.

## Server side

- Literally everything important was me -R
    - Specifically, websocket handling + http routing + html/js/css rendering (manually since aiohttp.web doesn't open new routes for js/css by default)
- I also helped -V
    - I refactored the GUI design (which was further refined by Aryan and Rohit) to make the interface streamlined.

## Extraneous 
- Server encryption: Paxton
- Discord handling: Rocco
- Discord bot integration: Gavin
