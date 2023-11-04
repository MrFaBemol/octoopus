from odoo.addons.music_library_api.utils.api import ApiAccess, ApiResponse




SUCCESS_VALID_TOKEN = ApiAccess(True, "Success")
ERROR_TOKEN_INVALID = ApiAccess(False, "Access denied: invalid access token.")
ERROR_NO_TOKEN = ApiAccess(False, "Access denied: missing access token.")





ERROR_RECORD_DOES_NOT_EXIST = ApiResponse(False, 404, "Record doesn't exist")
# ERROR_MISSING_POST_DATA = ApiResponse(False, "Error: your request misses required post data")






# Contains all the access log fields (like create_date) and the useless mixin fields
EXCLUDED_FIELDS = {
    'activity_ids', 'active', 'has_message', 'website_message_ids', 'message_ids', '__last_update', 'message_unread_counter', 'create_uid',
    'message_unread', 'my_activity_date_deadline', 'activity_exception_icon', 'activity_type_id', 'message_needaction_counter', 'message_attachment_count',
    'activity_summary', 'message_main_attachment_id', 'message_is_follower', 'message_has_error_counter', 'write_uid', 'activity_state',
    'activity_exception_decoration', 'message_follower_ids', 'create_date', 'activity_date_deadline', 'activity_type_icon', 'message_needaction',
    'message_partner_ids', 'message_has_error', 'activity_user_id', 'message_has_sms_error'
}
