
from django.db.models import Sum, F

from rest_framework.views import APIView
from rest_framework.response import Response

from accounts.permissions import IsTeacher
from students.models import Student
from batches.models import Batch
from attendance.models import Attendance
from fees.models import Fee


class ReportsView(APIView):

    permission_classes = [IsTeacher]

    def get(self, request):

        # ==========================================
        # BASIC COUNTS
        # ==========================================

        total_students = Student.objects.count()

        total_batches = Batch.objects.count()

        total_attendance = Attendance.objects.count()


        # ==========================================
        # ATTENDANCE
        # ==========================================

        present_count = Attendance.objects.filter(
            status=True
        ).count()

        absent_count = Attendance.objects.filter(
            status=False
        ).count()

        attendance_percentage = (
            round(
                (present_count / total_attendance) * 100,
                2
            )
            if total_attendance > 0
            else 0
        )


        # ==========================================
        # FEES
        # ==========================================

        fee_summary = Fee.objects.aggregate(
            total=Sum('total_amount'),
            paid=Sum('paid_amount')
        )

        total_fees = fee_summary['total'] or 0

        collected_fees = fee_summary['paid'] or 0

        pending_fees = total_fees - collected_fees


        pending_fee_students = Fee.objects.filter(
            paid_amount__lt=F('total_amount')
        ).count()


        # ==========================================
        # BATCH-WISE STUDENTS
        # ==========================================

        batch_report = []

        batches = Batch.objects.all().order_by('name')

        for batch in batches:

            student_count = Student.objects.filter(
                batch=batch
            ).count()

            batch_report.append({
                'id': batch.id,
                'name': batch.name,
                'student_count': student_count
            })


        # ==========================================
        # RECENT ATTENDANCE
        # ==========================================

        recent_attendance = []

        attendance_records = (
            Attendance.objects
            .select_related('student')
            .order_by('-date', 'student__name')[:10]
        )

        for record in attendance_records:

            recent_attendance.append({
                'id': record.id,
                'student_name': record.student.name,
                'date': record.date,
                'status': record.status
            })


        # ==========================================
        # RESPONSE
        # ==========================================

        return Response({

            'summary': {

                'total_students': total_students,

                'total_batches': total_batches,

                'total_attendance': total_attendance,

                'present_count': present_count,

                'absent_count': absent_count,

                'attendance_percentage':
                    attendance_percentage,

                'total_fees':
                    float(total_fees),

                'collected_fees':
                    float(collected_fees),

                'pending_fees':
                    float(pending_fees),

                'pending_fee_students':
                    pending_fee_students
            },

            'batch_report':
                batch_report,

            'recent_attendance':
                recent_attendance
        })

