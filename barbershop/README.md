# Barber Shop Management Module

## Overview

The Barber Shop Management module for Odoo provides a comprehensive solution for managing all aspects of a barbershop. From scheduling appointments to managing services, barbers, and customer interactions, this module streamlines operations and improves efficiency.

## Features

- **Customer Management**: Manage customer details and history.
- **Appointment Scheduling**: Schedule appointments with barbers, assign services, and track appointment status.
- **Barber Management**: Handle barber details, specialization, work schedules, and holidays.
- **Services Management**: Define and manage different services provided by the barbershop.
- **Bonuses**: Manage barber bonuses based on performance.
- **Reminders**: Set reminders for upcoming appointments.
- **Reporting**: Generate detailed reports on barber workloads, revenue, and services provided.
- **Email Notifications**: Automatically send email reminders to customers and barbers for upcoming appointments.
- **Support for Calendar Integration**: Integrates with the Odoo calendar for appointment management.

## Installation

1. Ensure you have a working Odoo instance with the necessary dependencies installed.
2. Clone or download the `barbershop` module into your Odoo `addons` directory.
3. Navigate to your Odoo instance and update the module list.
4. Install the "Barber Shop" module via the Apps menu.

## Dependencies

This module depends on the following Odoo core modules:
- `base`
- `mail`
- `contacts`
- `hr`
- `calendar`

External Python dependencies:
- `matplotlib`: Required for generating graphical reports.

## Configuration

### Security

The module includes specific security settings for managing access to different parts of the system. Ensure that users are assigned to the appropriate groups to gain access to the necessary features.

### Reports

The module provides the following reports:
- **Barber Load Report**: A comprehensive report detailing the workload of each barber, including the number of scheduled, completed, and canceled appointments, as well as revenue statistics.

### Email Templates

Custom email templates are provided for sending reminders and notifications:
- **Bonus Notification**: Notify barbers about their bonuses.
- **Appointment Reminder**: Remind customers and barbers of upcoming appointments.

## Usage

1. **Customers**: Manage customer records through the "Customers" menu.
2. **Appointments**: Schedule and manage appointments through the "Appointments" menu.
3. **Barbers**: Manage barbers, their work schedules, specializations, and holidays through the "Barbers" menu.
4. **Reports**: Generate and view detailed reports via the "Reporting" menu.
5. **Reminders**: Set up automatic reminders for appointments to keep both barbers and customers informed.

## Demo Data

For demonstration purposes, the module includes demo data that can be used to test and explore its features.

## Known Issues

- If any Python dependencies are missing, they need to be installed manually.

## License

This module is licensed under the LGPL-3.0 License. See the LICENSE file for more details.

## Author

- **Dmitriy Chumak** - [Barber Shop](http://www.barbershop.com/)

## Support

For any issues or support, please contact us at support@barbershop.com or visit our website.
