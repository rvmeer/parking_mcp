from mcp.server.fastmcp import FastMCP
#from parking_service import ParkingService
from parking_service_mock import ParkingServiceMock as ParkingService
import logging
import os
from datetime import datetime
from pathlib import Path

# Get absolute path to the script directory and create logs folder there
script_dir = Path(__file__).parent.absolute()
log_dir = script_dir / 'logs'
log_dir.mkdir(parents=True, exist_ok=True)

# Configure logging to file only (no console output)
log_filename = log_dir / f'parking_mcp_{datetime.now().strftime("%Y%m%d")}.log'

# Create logger and configure it without console output
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Only add file handler, no stream handler for console
file_handler = logging.FileHandler(log_filename)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

# Prevent propagation to root logger to avoid console output
logger.propagate = False

mcp = FastMCP("My App")

parking_service = ParkingService()

@mcp.tool()
def get_current_date() -> dict:
    """Get the current date in YYYY-MM-DD format"""
    logger.debug("get_current_date called")
    from datetime import datetime
    return {'date': datetime.now().strftime("%Y-%m-%d")}

@mcp.tool()
def get_current_user() -> dict:
    """Get the current user name"""
    #import getpass
    #return getpass.getuser()
    logger.debug("get_current_user called")
    return {'user': 'ralf@pipple.nl'}

# Get the amount of parking sport on a certain date
@mcp.tool()
def get_available_parking_spots_for_date(date: str) -> dict:
    """Get the number of available parking spots on a given date"""
    #global nr_of_parking_spots, taken_parking_spots

    #if date in taken_parking_spots:
    #    return nr_of_parking_spots - len(taken_parking_spots[date])
    #else:
    #    return nr_of_parking_spots
    logger.debug(f"get_available_parking_spots_for_date called with date: {date}")
    reservations = parking_service.get_reservations(date)
    available_parking_spots = 0
    if reservations:
        available_parking_spots = 4-len(reservations)
    else:
        available_parking_spots = 4

    return {'available_parking_spots': available_parking_spots}

@mcp.tool()
def get_reserved_parking_spots_for_date(date: str) -> list:
    """Get the list of reserved parking spots for a given date. Also contains the user and the reservation number."""
    
    #global taken_parking_spots
    #if date in taken_parking_spots:
    #    return taken_parking_spots[date]
    #else:
    #    return []
    logger.debug(f"get_reserved_parking_spots_for_date called with date: {date}")
    reservations = parking_service.get_reservations(date)
    if reservations:
        return reservations
    else:
        return []

@mcp.tool()
def reserve_parking_spot_for_date_and_user(date: str, user: str) -> dict:
    """Reserve a parking spot for a user on a given date"""
    
    # Do not reserve if not available and rserve if available
    #global taken_parking_spots
    #if date not in taken_parking_spots:
    #    taken_parking_spots[date] = []
    #if user in taken_parking_spots[date]:
    #    return f"Parking spot already reserved for {user} on {date}."
    #if len(taken_parking_spots[date]) >= nr_of_parking_spots:
    #    return f"No parking spots available on {date}."
    
    #taken_parking_spots[date].append(user)
    #return f"Parking spot reserved for {user} on {date}."
    logger.debug(f"reserve_parking_spot_for_date_and_user called with date: {date} and user: {user}")
    response = parking_service.reserve_parking_spot(date, "08:00", "17:00", user, is_customer=False)
    return {'response': response}

@mcp.tool()
def cancel_parking_spot_for_date_with_reservation_number(date: str, reservation_number: int) -> dict:
    """Cancel a parking spot reservation for a user on a given date"""
    
    #global taken_parking_spots
    #if date in taken_parking_spots and reservation_number < len(taken_parking_spots[date]):
    #    user = taken_parking_spots[date][reservation_number]
    #    del taken_parking_spots[date][reservation_number]
    #    return f"Parking spot reservation for {user} on {date} cancelled."
    #else:
    #    return f"No reservation found for number {reservation_number} on {date}."
    logger.debug(f"cancel_parking_spot_for_date_with_reservation_number called with date: {date} and reservation_number: {reservation_number}")
    response = parking_service.cancel_reservation(date, reservation_number)
    return {'response': response}

if __name__ == "__main__":
    logger.info("Starting MCP server...")
    mcp.run()
    # This will start the MCP server and make the tools available for use.