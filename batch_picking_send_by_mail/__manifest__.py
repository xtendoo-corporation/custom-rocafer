{
    "name": "Batch Picking by Mail",
    "summary": "Send batch picking by email",
    "version": "19.0.1.0.0",
    "author":
        "Salvador Gonzalez (Xtendoo)",
    "category": "Warehouse Management",
    "license": "AGPL-3",
    "depends": ["stock", "mail", "stock_picking_batch"],
    "data": [
        "views/stock_picking_batch_view.xml",
        "data/mail_template_data.xml"
    ],
    "installable": True,
}
