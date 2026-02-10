# Copyright (C) 2024 Manuel Calero (<https://xtendoo.es>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from math import ceil
from odoo import fields, models, api


class Product(models.Model):
    _inherit = "product.template"

    res_partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Name",
    )

    # num_partner = fields.Integer(
    #     string='Number partner'
    # )

    # num_order_partner = fields.Integer(
    #     string='Partner order number'
    # )

    label_code = fields.Char(string="Label code")

    # date_order = fields.Date(
    #     string='Date order'
    # )
    #
    # delivery_date = fields.Date(
    #     string='Delivery date'
    # )

    # register_by = fields.Char(
    #     string='Register by:'
    # )
    #
    # num_order = fields.Integer(
    #     string='Number order'
    # )

    troquel_number_1 = fields.Char(string="Troquel numero")

    troquel_number_2 = fields.Char(string="Troquel numero")

    troquel_figure_2 = fields.Integer(
        string="Figuras",
    )

    assembly_figure_x = fields.Integer(string="X width")

    assembly_figure_y = fields.Integer(string="Y height")

    troquel_figure = fields.Integer(
        string="Figures",
        compute="_calculate_troquel_figure",
        store=True,
    )

    @api.depends("assembly_figure_x", "assembly_figure_y")
    def _calculate_troquel_figure(self):
        for record in self:
            record.troquel_figure = record.assembly_figure_x * record.assembly_figure_y

    printing_cylinders = fields.Integer(string="Printing cylinders")

    cut_cylinders = fields.Integer(string="Cut cylinders")

    label_width = fields.Float(string="Label width")

    label_height = fields.Float(string="Label height")

    h1_value = fields.Float(
        string="H1 Value",
        default=lambda self: self.env.company.h1_value,
    )

    # @api.onchange('h1_value', 'label_width', 'printing_cylinder_size')
    # def compute_h1_value(self):
    #     for record in self:
    #         record.h1_value = record.printing_cylinder_size - record.label_width
    #         print("*"*80)
    #         if record.h1_value < self.env.company.h1_value:
    #             record.h1_value = self.env.company.h1_value

    h2_value = fields.Float(
        string="H2 Value",
        default=lambda self: self.env.company.h2_value,
    )

    # Nuevo campo
    v_value = fields.Float(
        string="V Value",
        compute="_compute_v_value",
    )

    @api.depends("label_height", "printing_cylinder_size")
    def _compute_v_value(self):
        for record in self:
            record.v_value = record.printing_cylinder_size - record.label_width

    amount = fields.Integer(
        string="Amount",
    )

    linear_meters = fields.Float(
        string="Linear meters", compute="_compute_meters", store=True
    )

    advance_label_separation = fields.Float(
        string="Advance label separation",
        compute="_compute_advance_label_separation",
        store=True,
    )

    @api.depends("label_width", "h1_value")
    def _compute_advance_label_separation(self):
        for record in self:
            record.advance_label_separation = record.label_width + record.h1_value

    @api.onchange("printing_cylinder_size")
    def _compute_printing_cylinder_id(self):
        for record in self:
            line_id = self.env["printing.cylinder.line"].search(
                [("size", ">=", record.advance_label_separation)],
                limit=1,
                order="size asc",
            )
            record.printing_cylinder_id = (
                line_id.printing_cylinder_id if line_id else False
            )

    printing_cylinder_id = fields.Many2one(
        comodel_name="printing.cylinder",
        string="Machine",
        default=_compute_printing_cylinder_id,
        store=True,
    )

    @api.depends("label_width")
    def _compute_printing_cylinder_size(self):
        for record in self:
            record.printing_cylinder_size = 0
            line_id = self.env["printing.cylinder.line"].search(
                [("size", ">=", record.label_width + self.env.company.h1_value)],
                limit=1,
                order="size asc",
            )
            if line_id:
                record.printing_cylinder_size = line_id.size

    printing_cylinder_size = fields.Float(
        string="Cylinder size", compute="_compute_printing_cylinder_size", store=True
    )

    @api.onchange("printing_cylinder_id")
    def _compute_z_impression_cylinder(self):
        for record in self:
            record.z_impression_cylinder = (
                record.printing_cylinder_id.z_impression_cylinder
            )

    z_impression_cylinder = fields.Integer(
        string="Z Impression cylinder",
        related="printing_cylinder_id.z_impression_cylinder",
    )

    @api.onchange("printing_cylinder_id")
    def _compute_z_magnetic_cut(self):
        for record in self:
            record.z_magnetic_cut = record.printing_cylinder_id.z_magnetic_cut

    z_magnetic_cut = fields.Integer(
        string="Z Magnetic Cut",
        related="printing_cylinder_id.z_magnetic_cut",
    )

    material_width_separation = fields.Integer(
        string="Material width separation",
        compute="_calculate_material_width_separation",
        store=True,
    )

    @api.depends("label_height", "assembly_figure_x", "h1_value", "h2_value")
    def _calculate_material_width_separation(self):
        for record in self:
            record.material_width_separation = (
                record.label_height * record.assembly_figure_x
                + record.h1_value * (record.assembly_figure_x - 1)
                + record.h2_value
            )

    product_material = fields.Many2one(
        comodel_name="material.type",
        string="Product material",
    )

    tolerance = fields.Float(
        string="Tolerancia en %",
    )

    @api.depends("assembly_figure_x", "printing_cylinder_size", "tolerance", "amount")
    def _compute_meters(self):
        for record in self:
            record.linear_meters = 0
            if record.assembly_figure_x:
                if record.tolerance == 0:
                    record.linear_meters = (
                        record.amount / 1000 * record.printing_cylinder_size
                    ) / record.assembly_figure_x
                else:
                    record.linear_meters = (
                        (record.amount / 1000 * record.printing_cylinder_size)
                        / record.assembly_figure_x
                        * (1 + record.tolerance / 100)
                    )
                record.linear_meters = ceil(
                    record.linear_meters / 1000
                )  # Convertir a metros

    # color_number = fields.Integer(
    #     string='Color numbers'
    # )

    amount_label_exit = fields.Integer(string="Amount label exit")

    inner_diameter_roll = fields.Integer(string="Inner diameter roll")

    outer_diameter_roll = fields.Integer(string="Outer diameter roll")

    print_orientation_id = fields.Many2one(
        comodel_name="print.orientation", string="Print orientation"
    )

    image_orientation = fields.Char(
        string="Imagen",
        related="print_orientation_id.image",
    )

    product_varnish = fields.Many2one(
        comodel_name="varnish.type",
        string="Product Varnish",
    )

    product_stamping = fields.Many2one(
        comodel_name="stamping.option",
        string="Product Stamping",
    )

    serigraphy = fields.Boolean(
        string="Serigraphy",
    )

    relief = fields.Boolean(
        string="Relief",
    )

    laminated = fields.Selection(
        selection=[
            ("gloss", "Brillo"),
            ("matte", "Mate"),
        ],
        string="Laminated",
    )

    other_finishes = fields.Char(
        string="Other finishes",
    )

    preprint_comments = fields.Char(
        string="Preprint comments",
    )

    administration_comments = fields.Char(string="Administration Comments")

    reviewers_expedition = fields.Char(string="Reviewers/Expedition")

    color_ink_ids = fields.One2many(
        comodel_name="color.ink",
        inverse_name="product_template_id",
        string="Colors ink",
    )

    ink_count = fields.Integer(
        string="Numero de colores",
        compute="_compute_ink_count",
        store=True,
    )

    engravings_number = fields.Integer(string="Número de grabados")

    quantity_label_roll = fields.Integer(string="Canditad de etiquetas por rollo")

    @api.depends("color_ink_ids")
    def _compute_ink_count(self):
        for record in self:
            record.ink_count = len(record.color_ink_ids)

    regulatory_council_numbering = fields.Boolean(string="Regulatory council numbering")
