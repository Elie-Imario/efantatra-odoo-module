# -*- coding: utf-8 -*-
# from odoo import http


# class Efantatra(http.Controller):
#     @http.route('/efantatra/efantatra', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/efantatra/efantatra/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('efantatra.listing', {
#             'root': '/efantatra/efantatra',
#             'objects': http.request.env['efantatra.efantatra'].search([]),
#         })

#     @http.route('/efantatra/efantatra/objects/<model("efantatra.efantatra"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('efantatra.object', {
#             'object': obj
#         })
