{
    "name": "rocafer_custom_report",
    "summary": """Formatos de documentos Rocafer""",
    "version": "19.0.1.0.0",
    "description": """Formatos de documentos Rocafer""",
    "company": "Xtendoo",
    "website": "http://www.xtendoo.es",
    "category": "Warehouse Management",
    "depends": [
        'stock',
        'stock_picking_report_valued',
        'stock_picking_batch',
    ],
    "license": "AGPL-3",
    "data": [
        "reports/stock_picking_report_valued.xml",
        "reports/stock_package_report.xml",
        "reports/sale_order_report.xml",
        "reports/invoice_document_report.xml",
        "views/stock_picking_view.xml",
    ],
    "installable": True,
}
