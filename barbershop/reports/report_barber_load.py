import base64
import io
import matplotlib.pyplot as plt
from datetime import date
from odoo import models, api


class AppointmentReport(models.AbstractModel):
    _name = 'report.barbershop.report_barber_load'
    _description = 'Barber Load Report'

    def _generate_pie_chart(self, sizes, labels, colors):
        """
        Generate a pie chart from the given sizes, labels, and colors.
        Returns a base64 encoded image.
        """
        fig, ax = plt.subplots(figsize=(4, 4))
        ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        # Adding a shadow and increasing contrast
        plt.subplots_adjust(left=0, right=1, top=1, bottom=0)  # Ensure nothing is cut off
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')  # Save the figure as PNG
        plt.close(fig)
        buf.seek(0)
        return base64.b64encode(buf.read()).decode('utf-8')

    @api.model
    def _get_report_values(self, docids, data=None):
        today = date.today()
        date_start = data.get('date_start') or date(today.year, 1, 1)
        date_end = data.get('date_end') or date(today.year, 12, 31)

        appointments = self.env['barbershop.appointment'].search([
            ('date_time', '>=', date_start),
            ('date_time', '<=', date_end)
        ])

        grouped_appointments = {}
        total_scheduled = total_completed = total_cancelled = 0
        total_scheduled_revenue = total_completed_revenue = 0.0

        for appointment in appointments:
            barber = appointment.employee_id
            if barber not in grouped_appointments:
                grouped_appointments[barber] = {
                    'appointments': [],
                    'scheduled_count': 0,
                    'completed_count': 0,
                    'canceled_count': 0,
                    'total_completed_revenue': 0.0,
                    'total_scheduled_revenue': 0.0,
                    'chart_image': None,
                    'services': {}
                }

            grouped_appointments[barber]['appointments'].append(appointment)

            if appointment.state == 'scheduled':
                grouped_appointments[barber]['scheduled_count'] += 1
                grouped_appointments[barber]['total_scheduled_revenue'] += appointment.service_cost
                total_scheduled += 1
                total_scheduled_revenue += appointment.service_cost
            elif appointment.state == 'completed':
                grouped_appointments[barber]['completed_count'] += 1
                grouped_appointments[barber]['total_completed_revenue'] += appointment.service_cost
                total_completed += 1
                total_completed_revenue += appointment.service_cost
            elif appointment.state == 'cancelled':
                grouped_appointments[barber]['canceled_count'] += 1
                total_cancelled += 1

            service_name = appointment.service_id.name
            if service_name not in grouped_appointments[barber]['services']:
                grouped_appointments[barber]['services'][service_name] = {
                    'count': 0,
                    'revenue': 0.0
                }
            grouped_appointments[barber]['services'][service_name]['count'] += 1
            grouped_appointments[barber]['services'][service_name]['revenue'] += appointment.service_cost

        overall_sizes = [total_scheduled or 0, total_completed or 0, total_cancelled or 0]

        if any(overall_sizes):
            overall_labels = ['Scheduled', 'Completed', 'Cancelled']
            overall_colors = ['#66C2A5', '#FC8D62', '#8DA0CB']
            total_chart_image = self._generate_pie_chart(overall_sizes, overall_labels, overall_colors)
        else:
            total_chart_image = None

        for barber, data in grouped_appointments.items():
            sizes = [
                data['scheduled_count'] or 0,
                data['completed_count'] or 0,
                data['canceled_count'] or 0
            ]

            if any(sizes):
                labels = ['Scheduled', 'Completed', 'Cancelled']
                colors = ['#66C2A5', '#FC8D62', '#8DA0CB']
                data['chart_image'] = self._generate_pie_chart(sizes, labels, colors)
            else:
                data['chart_image'] = None

        return {
            'doc_ids': docids,
            'doc_model': 'barbershop.appointment',
            'total_scheduled': total_scheduled,
            'total_completed': total_completed,
            'total_cancelled': total_cancelled,
            'total_scheduled_revenue': total_scheduled_revenue,
            'total_completed_revenue': total_completed_revenue,
            'total_chart_image': total_chart_image,
            'grouped_appointments': grouped_appointments,
        }
