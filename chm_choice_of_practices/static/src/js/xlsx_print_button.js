/** @odoo-module **/

document.addEventListener('DOMContentLoaded', function() {

    if (typeof odoo !== 'undefined' && odoo.session_info) {

        if (!odoo.session_info.user_has_group('base.group_system')) {
            const leftPanel = document.querySelector('.o_cp_bottom_left');
            if (leftPanel) {
                leftPanel.style.display = 'none';
            }
        }
    }
});