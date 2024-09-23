from django.contrib import admin
from .models import Member, Employee, Business, Badge

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'id', 'role', 'platform', 'created_at', 'updated_at')
    search_fields = ('user__username', 'nzid', 'role', 'platform')
    list_filter = ('role', 'platform', 'status')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('user', 'role', 'age', 'status')

# Employee Admin
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'job_department', 'job_title', 'platform', 'created_at', 'updated_at')
    search_fields = ('user__username', 'role', 'job_department', 'job_title', 'platform')
    list_filter = ('role', 'job_department', 'platform', 'status')
    readonly_fields = ('created_at', 'updated_at')

# Business Admin
@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ('name', 'industry', 'platform', 'registration_date', 'created_at', 'updated_at')
    search_fields = ('name', 'industry', 'platform', 'email', 'phone')
    list_filter = ('industry', 'platform', 'status')
    readonly_fields = ('created_at', 'updated_at', 'registration_date')
    #  filter_horizontal = ('owners',)  To make selecting multiple owners easier

# Badge Admin
@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'business', 'platform', 'issued_date', 'expiry_date', 'updated_at')
    search_fields = ('name', 'type', 'business__name', 'platform')
    list_filter = ('type', 'platform', 'status')
    readonly_fields = ('issued_date', 'updated_at')