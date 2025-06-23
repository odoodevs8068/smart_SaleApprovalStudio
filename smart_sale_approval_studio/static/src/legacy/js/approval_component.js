odoo.define('smart_sale_approval_studio.ApprovalComponentPatch', function (require) {
    'use strict';

    const ApprovalComponent = require('web_studio.ApprovalComponent');

    console.log("ApprovalComponent Patch Loaded");

    // Backup the original method if needed
    const originalFetchApprovalData = ApprovalComponent.prototype._fetchApprovalData;

    // Override the method directly
    ApprovalComponent.prototype._fetchApprovalData = async function () {
        console.log("ApprovalComponent _fetchApprovalData overridden");

        const spec = await this.rpc(
            {
                model: 'studio.approval.rule',
                method: 'get_approval_spec',
                args: [this.props.model, this.props.method, this.props.action],
                kwargs: {
                    res_id: !this.props.inStudio && this.props.resId,
                },
                context: {
                    ...this.env.session.user_context,
                    active_id: this.props.resId,
                },
            },
            { shadow: true }
        );

        spec.entries.forEach((entry) => {
            entry.long_date = moment.utc(entry.write_date).local().format('LLL');
            entry.short_date = moment.utc(entry.write_date).local().format('LL');
        });

        Object.assign(this.state, spec);
        this.state.init = false;
    };
});
