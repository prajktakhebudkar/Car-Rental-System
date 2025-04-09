import datetime
from enum import Enum
from typing import List, Dict, Optional


class RentalBasis(Enum):
    """Enum representing different rental time periods."""
    HOURLY = 1
    DAILY = 2
    WEEKLY = 3


class Car:
    """Class representing a car in the rental system."""
    
    def __init__(self, car_id: str, model: str, price_hourly: float, price_daily: float, price_weekly: float):
        """Initialize a new Car object.
        
        Args:
            car_id: Unique identifier for the car
            model: Car model name
            price_hourly: Hourly rental price
            price_daily: Daily rental price
            price_weekly: Weekly rental price
        """
        self.car_id = car_id
        self.model = model
        self.price_hourly = price_hourly
        self.price_daily = price_daily
        self.price_weekly = price_weekly
        self.available = True
        self.rental_start_time = None
        self.rental_basis = None
    
    def __str__(self) -> str:
        """Return string representation of the car."""
        status = "Available" if self.available else "Not Available"
        return f"Car ID: {self.car_id} | Model: {self.model} | Status: {status}"


class Customer:
    """Class representing a customer in the rental system."""
    
    def __init__(self, customer_id: str, name: str, email: str, phone: str):
        """Initialize a new Customer object.
        
        Args:
            customer_id: Unique identifier for the customer
            name: Customer name
            email: Customer email
            phone: Customer phone number
        """
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.phone = phone
        self.rented_cars = []
        self.rental_history = []
    
    def __str__(self) -> str:
        """Return string representation of the customer."""
        return f"Customer ID: {self.customer_id} | Name: {self.name} | Email: {self.email}"


class Rental:
    """Class representing a rental transaction."""
    
    def __init__(self, rental_id: str, customer: Customer, cars: List[Car], rental_basis: RentalBasis):
        """Initialize a new Rental object.
        
        Args:
            rental_id: Unique identifier for the rental
            customer: Customer who is renting
            cars: List of cars being rented
            rental_basis: Basis of rental (hourly, daily, weekly)
        """
        self.rental_id = rental_id
        self.customer = customer
        self.cars = cars
        self.rental_basis = rental_basis
        self.start_time = datetime.datetime.now()
        self.end_time = None
        self.bill_amount = 0.0
    
    def calculate_bill(self) -> float:
        """Calculate the bill amount based on rental duration and basis."""
        if not self.end_time:
            self.end_time = datetime.datetime.now()
        
        rental_duration = self.end_time - self.start_time
        
        if self.rental_basis == RentalBasis.HOURLY:
            hours = max(1, int(rental_duration.total_seconds() / 3600))
            self.bill_amount = sum(car.price_hourly * hours for car in self.cars)
        
        elif self.rental_basis == RentalBasis.DAILY:
            days = max(1, int(rental_duration.total_seconds() / (24 * 3600)))
            self.bill_amount = sum(car.price_daily * days for car in self.cars)
        
        elif self.rental_basis == RentalBasis.WEEKLY:
            weeks = max(1, int(rental_duration.total_seconds() / (7 * 24 * 3600)))
            self.bill_amount = sum(car.price_weekly * weeks for car in self.cars)
        
        return self.bill_amount


class Bill:
    """Class representing a bill for a rental."""
    
    def __init__(self, bill_id: str, rental: Rental):
        """Initialize a new Bill object.
        
        Args:
            bill_id: Unique identifier for the bill
            rental: Rental associated with the bill
        """
        self.bill_id = bill_id
        self.rental = rental
        self.amount = rental.calculate_bill()
        self.generated_time = datetime.datetime.now()
        self.paid = False
    
    def mark_as_paid(self):
        """Mark the bill as paid."""
        self.paid = True
    
    def generate_invoice(self) -> str:
        """Generate a readable invoice."""
        rental_basis_str = self.rental.rental_basis.name.lower()
        duration = (self.rental.end_time - self.rental.start_time).total_seconds()
        
        if self.rental.rental_basis == RentalBasis.HOURLY:
            duration_units = max(1, int(duration / 3600))
            unit_str = "hour(s)"
        elif self.rental.rental_basis == RentalBasis.DAILY:
            duration_units = max(1, int(duration / (24 * 3600)))
            unit_str = "day(s)"
        else:
            duration_units = max(1, int(duration / (7 * 24 * 3600)))
            unit_str = "week(s)"
        
        invoice = f"""
        ======= INVOICE =======
        Bill ID: {self.bill_id}
        Customer: {self.rental.customer.name}
        
        Rental Details:
        - Rental ID: {self.rental.rental_id}
        - Rental Basis: {rental_basis_str}
        - Duration: {duration_units} {unit_str}
        - Start Time: {self.rental.start_time.strftime('%Y-%m-%d %H:%M:%S')}
        - End Time: {self.rental.end_time.strftime('%Y-%m-%d %H:%M:%S')}
        
        Cars Rented:
        """
        
        for car in self.rental.cars:
            invoice += f"- Car ID: {car.car_id} | Model: {car.model}\n"
        
        invoice += f"""
        Total Amount: ${self.amount:.2f}
        Status: {"Paid" if self.paid else "Unpaid"}
        
        Generated on: {self.generated_time.strftime('%Y-%m-%d %H:%M:%S')}
        =======================
        """
        
        return invoice


class CarRentalSystem:
    """Main class for the car rental system."""
    
    def __init__(self, company_name: str):
        """Initialize a new CarRentalSystem.
        
        Args:
            company_name: Name of the car rental company
        """
        self.company_name = company_name
        self.inventory: Dict[str, Car] = {}
        self.customers: Dict[str, Customer] = {}
        self.rentals: Dict[str, Rental] = {}
        self.bills: Dict[str, Bill] = {}
        self.rental_counter = 0
        self.bill_counter = 0
    
    def add_car(self, car: Car) -> bool:
        """Add a car to the inventory.
        
        Args:
            car: Car object to add
            
        Returns:
            bool: True if addition successful, False otherwise
        """
        if car.car_id in self.inventory:
            print(f"Car with ID {car.car_id} already exists in inventory.")
            return False
        
        self.inventory[car.car_id] = car
        print(f"Car with ID {car.car_id} added to inventory successfully.")
        return True
    
    def add_customer(self, customer: Customer) -> bool:
        """Add a customer to the system.
        
        Args:
            customer: Customer object to add
            
        Returns:
            bool: True if addition successful, False otherwise
        """
        if customer.customer_id in self.customers:
            print(f"Customer with ID {customer.customer_id} already exists.")
            return False
        
        self.customers[customer.customer_id] = customer
        print(f"Customer with ID {customer.customer_id} added successfully.")
        return True
    
    def display_available_cars(self) -> List[Car]:
        """Display all available cars.
        
        Returns:
            List[Car]: List of available cars
        """
        available_cars = [car for car in self.inventory.values() if car.available]
        
        if not available_cars:
            print("No cars are currently available for rent.")
            return []
        
        print(f"\nAvailable Cars ({len(available_cars)}):")
        print("=" * 50)
        for car in available_cars:
            print(f"{car}")
            print(f"   Hourly Rate: ${car.price_hourly:.2f} | Daily Rate: ${car.price_daily:.2f} | Weekly Rate: ${car.price_weekly:.2f}")
        print("=" * 50)
        
        return available_cars
    
    def find_customer(self, customer_id: str) -> Optional[Customer]:
        """Find a customer by ID.
        
        Args:
            customer_id: ID of the customer to find
            
        Returns:
            Optional[Customer]: Customer object if found, None otherwise
        """
        if customer_id in self.customers:
            return self.customers[customer_id]
        
        print(f"Customer with ID {customer_id} not found.")
        return None
    
    def rent_cars(self, customer_id: str, car_ids: List[str], rental_basis: RentalBasis) -> Optional[Rental]:
        """Rent cars to a customer.
        
        Args:
            customer_id: ID of the customer renting cars
            car_ids: List of car IDs to rent
            rental_basis: Basis of rental (hourly, daily, weekly)
            
        Returns:
            Optional[Rental]: Rental object if successful, None otherwise
        """
        customer = self.find_customer(customer_id)
        if not customer:
            return None
        
        cars_to_rent = []
        for car_id in car_ids:
            if car_id not in self.inventory:
                print(f"Car with ID {car_id} does not exist in inventory.")
                return None
            
            car = self.inventory[car_id]
            if not car.available:
                print(f"Car with ID {car_id} is not available for rent.")
                return None
            
            cars_to_rent.append(car)
        
        # Generate rental ID
        self.rental_counter += 1
        rental_id = f"R{self.rental_counter:04d}"
        
        # Create rental
        rental = Rental(rental_id, customer, cars_to_rent, rental_basis)
        self.rentals[rental_id] = rental
        
        # Update car status
        for car in cars_to_rent:
            car.available = False
            car.rental_start_time = rental.start_time
            car.rental_basis = rental_basis
        
        # Update customer rentals
        customer.rented_cars.extend(cars_to_rent)
        
        basis_str = rental_basis.name.lower()
        print(f"\nCars rented successfully on a {basis_str} basis.")
        print(f"Rental ID: {rental_id}")
        print(f"Start Time: {rental.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Number of cars rented: {len(cars_to_rent)}")
        
        return rental
    
    def return_cars(self, rental_id: str) -> Optional[Bill]:
        """Return rented cars and generate bill.
        
        Args:
            rental_id: ID of the rental to return
            
        Returns:
            Optional[Bill]: Bill object if successful, None otherwise
        """
        if rental_id not in self.rentals:
            print(f"Rental with ID {rental_id} not found.")
            return None
        
        rental = self.rentals[rental_id]
        rental.end_time = datetime.datetime.now()
        
        # Update car status
        for car in rental.cars:
            car.available = True
            car.rental_start_time = None
            car.rental_basis = None
        
        # Update customer rentals
        for car in rental.cars:
            if car in rental.customer.rented_cars:
                rental.customer.rented_cars.remove(car)
        
        rental.customer.rental_history.append(rental)
        
        # Generate bill
        self.bill_counter += 1
        bill_id = f"B{self.bill_counter:04d}"
        bill = Bill(bill_id, rental)
        self.bills[bill_id] = bill
        
        print(f"\nCars returned successfully.")
        print(f"Rental ID: {rental_id}")
        print(f"End Time: {rental.end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Bill ID: {bill_id}")
        print(f"Amount: ${bill.amount:.2f}")
        
        return bill


# Example usage
def main():
    # Initialize the system
    car_rental_system = CarRentalSystem("FastWheels Car Rental")
    
    # Add cars to inventory
    car1 = Car("C001", "Toyota Camry", 10.0, 50.0, 300.0)
    car2 = Car("C002", "Honda Civic", 8.0, 45.0, 280.0)
    car3 = Car("C003", "Ford Mustang", 15.0, 75.0, 450.0)
    car4 = Car("C004", "Tesla Model 3", 20.0, 100.0, 600.0)
    car5 = Car("C005", "BMW X5", 25.0, 120.0, 700.0)
    
    car_rental_system.add_car(car1)
    car_rental_system.add_car(car2)
    car_rental_system.add_car(car3)
    car_rental_system.add_car(car4)
    car_rental_system.add_car(car5)
    
    # Add customers
    customer1 = Customer("CUST001", "John Doe", "john.doe@example.com", "123-456-7890")
    customer2 = Customer("CUST002", "Jane Smith", "jane.smith@example.com", "098-765-4321")
    
    car_rental_system.add_customer(customer1)
    car_rental_system.add_customer(customer2)
    
    # Display available cars
    car_rental_system.display_available_cars()
    
    # Customer1 rents cars on hourly basis
    rental1 = car_rental_system.rent_cars("CUST001", ["C001", "C002"], RentalBasis.HOURLY)
    
    # Display available cars after rental
    car_rental_system.display_available_cars()
    
    # Simulate passage of time (3 hours)
    rental1.start_time = rental1.start_time - datetime.timedelta(hours=3)
    
    # Return cars
    bill1 = car_rental_system.return_cars(rental1.rental_id)
    
    # Display bill
    if bill1:
        print(bill1.generate_invoice())
    
    # Display available cars after return
    car_rental_system.display_available_cars()
    
    # Customer2 rents cars on daily basis
    rental2 = car_rental_system.rent_cars("CUST002", ["C003", "C004", "C005"], RentalBasis.DAILY)
    
    # Simulate passage of time (2 days)
    rental2.start_time = rental2.start_time - datetime.timedelta(days=2)
    
    # Return cars
    bill2 = car_rental_system.return_cars(rental2.rental_id)
    
    # Display bill
    if bill2:
        print(bill2.generate_invoice())


if __name__ == "__main__":
    main() 