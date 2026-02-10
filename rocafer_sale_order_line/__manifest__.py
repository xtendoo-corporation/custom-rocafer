{
    "name": "rocafer_sale_order_line",
    "summary": """Sales Order Line Custom""",
    "version": "18.0.1.0.0",
    "description": """Sales Order Line Custom""",
    "company": "Xtendoo",
    "website": "http://www.xtendoo.es",
    "category": "Warehouse Management",
    "depends": ["product", "rocafer_product_template_report", "sale"],
    "license": "AGPL-3",
    "data": [
        "views/sale_order_line_view.xml",
        "views/stock_picking_form_view.xml",
    ],
    "installable": True,
}
