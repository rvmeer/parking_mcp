import logging
from typing import List, Dict, Any
from datetime import datetime
import pathlib
import os

# Get absolute path to the script directory and create logs folder there
script_dir = pathlib.Path(__file__).parent.absolute()
log_dir = script_dir / 'logs'
log_dir.mkdir(parents=True, exist_ok=True)

# Configure logging - file only, no console output
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Only add file handler, no stream handler for console
file_handler = logging.FileHandler(log_dir / 'parking_service_mock.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

# Prevent propagation to root logger to avoid console output
logger.propagate = False



class ParkingServiceMock:
    def __init__(self, base_url: str = "https://pippleparkingapp.azurewebsites.net/api"):
        self.BASE_URL = base_url
        self.reservations: Dict[str, List[Dict[str, Any]]] = {}
        self.next_reservation_number = 0
        logger.info(f"ParkingServiceMock initialized with base_url: {base_url}")

    def reserve_parking_spot(self, date: str, start_time: str, end_time: str, email: str, is_customer: bool) -> str:
        """Reserve a parking spot for a given date and time."""
        logger.info(f"reserve_parking_spot called - Date: {date}, Start: {start_time}, End: {end_time}, Email: {email}, Customer: {is_customer}")
        
        # Initialize date if not exists
        if date not in self.reservations:
            self.reservations[date] = []
        
        # Create reservation
        reservation = {
            "Email": email,
            "Begintijd": start_time + ":00" if len(start_time) == 5 else start_time,
            "Eindtijd": end_time + ":00" if len(end_time) == 5 else end_time,
            "Klant": is_customer,
            "Reserveringsnummer": self.next_reservation_number,
            "Datum": self._date_to_timestamp(date)
        }
        
        self.reservations[date].append(reservation)
        self.next_reservation_number += 1
        
        response = f"Reservation created successfully. Reservation number: {reservation['Reserveringsnummer']}"
        logger.info(f"Reservation created: {response}")
        return response

    def get_reservations(self, date: str) -> List[Dict[str, Any]]:
        """Get reservations for a specific date."""
        logger.info(f"get_reservations called for date: {date}")
        
        reservations = self.reservations.get(date, [])
        logger.info(f"Found {len(reservations)} reservations for {date}")
        return reservations

    def cancel_reservation(self, date: str, reservation_number: int) -> str:
        """Cancel a reservation by date and reservation number."""
        logger.info(f"cancel_reservation called - Date: {date}, Reservation number: {reservation_number}")
        
        if date not in self.reservations:
            response = f"No reservations found for date {date}"
            logger.warning(response)
            return response
        
        # Find and remove reservation
        for i, reservation in enumerate(self.reservations[date]):
            if reservation["Reserveringsnummer"] == reservation_number:
                removed_reservation = self.reservations[date].pop(i)
                response = f"Reservation {reservation_number} cancelled successfully"
                logger.info(f"Reservation cancelled: {removed_reservation}")
                return response
        
        response = f"Reservation {reservation_number} not found for date {date}"
        logger.warning(response)
        return response

    def _date_to_timestamp(self, date_str: str) -> int:
        """Convert date string to timestamp (mimicking API behavior)."""
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            return int(dt.timestamp() * 1000)  # Convert to milliseconds
        except ValueError:
            logger.error(f"Invalid date format: {date_str}")
            return 0

    def get_all_reservations(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get all reservations (helper method for testing)."""
        logger.info("get_all_reservations called")
        return self.reservations.copy()

    def clear_all_reservations(self) -> str:
        """Clear all reservations (helper method for testing)."""
        logger.info("clear_all_reservations called")
        self.reservations.clear()
        self.next_reservation_number = 0
        return "All reservations cleared"
