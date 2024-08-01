import subprocess
import time

def start_redis_server():
    """Start the Redis server."""
    redis_server_path = 'redis-server'  # Update if necessary to full path

    # Start the Redis server process
    process = subprocess.Popen([redis_server_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Wait for a short while to ensure Redis has started
    time.sleep(2)

    return process

def stop_redis_server(process):
    """Stop the Redis server."""
    process.terminate()  # Gracefully stop the server
    process.wait()

if __name__ == "__main__":
    print("Starting Redis server...")
    redis_process = start_redis_server()
    
    # Run your application or tests here while Redis is running
    print("Redis server started. Press Enter to stop...")
    input()  # Wait for user input to stop the server
    
    print("Stopping Redis server...")
    stop_redis_server(redis_process)
    print("Redis server stopped.")
