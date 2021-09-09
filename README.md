# pi-client

# Post Ex

Example for sending post requests with data logs

## Usage
```python
client = RockDetection("http://localhost:5000/data") # sets the default post route to the string given
client.send_post(data={'data': 'something'}) #sends data to post route
```