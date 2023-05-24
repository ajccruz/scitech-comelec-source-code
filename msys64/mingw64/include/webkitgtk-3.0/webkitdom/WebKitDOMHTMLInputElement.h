/*
 *  This file is part of the WebKit open source project.
 *  This file has been generated by generate-bindings.pl. DO NOT MODIFY!
 *
 *  This library is free software; you can redistribute it and/or
 *  modify it under the terms of the GNU Library General Public
 *  License as published by the Free Software Foundation; either
 *  version 2 of the License, or (at your option) any later version.
 *
 *  This library is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 *  Library General Public License for more details.
 *
 *  You should have received a copy of the GNU Library General Public License
 *  along with this library; see the file COPYING.LIB.  If not, write to
 *  the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
 *  Boston, MA 02110-1301, USA.
 */

#if !defined(__WEBKITDOM_H_INSIDE__) && !defined(BUILDING_WEBKIT)
#error "Only <webkitdom/webkitdom.h> can be included directly."
#endif

#ifndef WebKitDOMHTMLInputElement_h
#define WebKitDOMHTMLInputElement_h

#include <glib-object.h>
#include <webkitdom/WebKitDOMHTMLElement.h>
#include <webkitdom/webkitdomdefines.h>

G_BEGIN_DECLS

#define WEBKIT_TYPE_DOM_HTML_INPUT_ELEMENT            (webkit_dom_html_input_element_get_type())
#define WEBKIT_DOM_HTML_INPUT_ELEMENT(obj)            (G_TYPE_CHECK_INSTANCE_CAST((obj), WEBKIT_TYPE_DOM_HTML_INPUT_ELEMENT, WebKitDOMHTMLInputElement))
#define WEBKIT_DOM_HTML_INPUT_ELEMENT_CLASS(klass)    (G_TYPE_CHECK_CLASS_CAST((klass),  WEBKIT_TYPE_DOM_HTML_INPUT_ELEMENT, WebKitDOMHTMLInputElementClass)
#define WEBKIT_DOM_IS_HTML_INPUT_ELEMENT(obj)         (G_TYPE_CHECK_INSTANCE_TYPE((obj), WEBKIT_TYPE_DOM_HTML_INPUT_ELEMENT))
#define WEBKIT_DOM_IS_HTML_INPUT_ELEMENT_CLASS(klass) (G_TYPE_CHECK_CLASS_TYPE((klass),  WEBKIT_TYPE_DOM_HTML_INPUT_ELEMENT))
#define WEBKIT_DOM_HTML_INPUT_ELEMENT_GET_CLASS(obj)  (G_TYPE_INSTANCE_GET_CLASS((obj),  WEBKIT_TYPE_DOM_HTML_INPUT_ELEMENT, WebKitDOMHTMLInputElementClass))

struct _WebKitDOMHTMLInputElement {
    WebKitDOMHTMLElement parent_instance;
};

struct _WebKitDOMHTMLInputElementClass {
    WebKitDOMHTMLElementClass parent_class;
};

WEBKIT_API GType
webkit_dom_html_input_element_get_type (void);

/**
 * webkit_dom_html_input_element_step_up:
 * @self: A #WebKitDOMHTMLInputElement
 * @n: A #glong
 * @error: #GError
 *
**/
WEBKIT_API void
webkit_dom_html_input_element_step_up(WebKitDOMHTMLInputElement* self, glong n, GError** error);

/**
 * webkit_dom_html_input_element_step_down:
 * @self: A #WebKitDOMHTMLInputElement
 * @n: A #glong
 * @error: #GError
 *
**/
WEBKIT_API void
webkit_dom_html_input_element_step_down(WebKitDOMHTMLInputElement* self, glong n, GError** error);

/**
 * webkit_dom_html_input_element_check_validity:
 * @self: A #WebKitDOMHTMLInputElement
 *
 * Returns: A #gboolean
**/
WEBKIT_API gboolean
webkit_dom_html_input_element_check_validity(WebKitDOMHTMLInputElement* self);

/**
 * webkit_dom_html_input_element_set_custom_validity:
 * @self: A #WebKitDOMHTMLInputElement
 * @error: A #gchar
 *
**/
WEBKIT_API void
webkit_dom_html_input_element_set_custom_validity(WebKitDOMHTMLInputElement* self, const gchar* error);

/**
 * webkit_dom_html_input_element_select:
 * @self: A #WebKitDOMHTMLInputElement
 *
**/
WEBKIT_API void
webkit_dom_html_input_element_select(WebKitDOMHTMLInputElement* self);

/**
 * webkit_dom_html_input_element_set_range_text:
 * @self: A #WebKitDOMHTMLInputElement
 * @replacement: A #gchar
 * @start: A #gulong
 * @end: A #gulong
 * @selectionMode: A #gchar
 * @error: #GError
 *
**/
WEBKIT_API void
webkit_dom_html_input_element_set_range_text(WebKitDOMHTMLInputElement* self, const gchar* replacement, gulong start, gulong end, const gchar* selectionMode, GError** error);

/**
 * webkit_dom_html_input_element_set_value_for_user:
 * @self: A #WebKitDOMHTMLInputElement
 * @value: A #gchar
 *
**/
WEBKIT_API void
webkit_dom_html_input_element_set_value_for_user(WebKitDOMHTMLInputElement* self, const gchar* value);

/**
 * webkit_dom_html_input_element_get_accept:
 * @self: A #WebKitDOMHTMLInputElement
 *
 * Returns: A #gchar
**/
WEBKIT_API gchar*
webkit_dom_html_input_element_get_accept(WebKitDOMHTMLInputElement* self);

/**
 * webkit_dom_html_input_element_set_accept:
 * @self: A #WebKitDOMHTMLInputElement
 * @value: A #gchar
 *
**/
WEBKIT_API void
webkit_dom_html_input_element_set_accept(WebKitDOMHTMLInputElement* self, const gchar* value);

/**
 * webkit_dom_html_input_element_get_alt:
 * @self: A #WebKitDOMHTMLInputElement
 *
 * Returns: A #gchar
**/
WEBKIT_API gchar*
webkit_dom_html_input_element_get_alt(WebKitDOMHTMLInputElement* self);

/**
 * webkit_dom_html_input_element_set_alt:
 * @self: A #WebKitDOMHTMLInputElement
 * @value: A #gchar
 *
**/
WEBKIT_API void
webkit_dom_html_input_element_set_alt(WebKitDOMHTMLInputElement* self, const gchar* value);

/**
 * webkit_dom_html_input_element_get_autocomplete:
 * @self: A #WebKitDOMHTMLInputElement
 *
 * Returns: A #gchar
**/
WEBKIT_API gchar*
webkit_dom_html_input_element_get_autocomplete(WebKitDOMHTMLInputElement* self);

/**
 * webkit_dom_html_input_element_set_autocomplete:
 * @self: A #WebKitDOMHTMLInputElement
 * @value: A #gchar
 *
**/
WEBKIT_API void
webkit_dom_html_input_element_set_autocomplete(WebKitDOMHTMLInputElement* self, const gchar* value);

/**
 * webkit_dom_html_input_element_get_autofocus:
 * @self: A #WebKitDOMHTMLInputElement
 *
 * Returns: A #gboolean
**/
WEBKIT_API gboolean
webkit_dom_html_input_element_get_autofocus(WebKitDOMHTMLInputElement* self);

/**
 * webkit_dom_html_input_element_set_autofocus:
 * @self: A #WebKitDOMHTMLInputElement
 * @value: A #gboolean
 *
**/
WEBKIT_API void
webkit_dom_html_input_element_set_autofocus(WebKitDOMHTMLInputElement* self, gboolean value);

/**
 * webkit_dom_html_input_element_get_default_checked:
 * @self: A #WebKitDOMHTMLInputElement
 *
 * Returns: A #gboolean
**/
WEBKIT_API gboolean
webkit_dom_html_input_element_get_default_checked(WebKitDOMHTMLInputElement* self);

/**
 * webkit_dom_html_input_element_set_default_checked:
 * @self: A #WebKitDOMHTMLInputElement
 * @value: A #gboolean
 *
**/
WEBKIT_API void
webkit_dom_html_input_element_set_default_checked(WebKitDOMHTMLInputElement* self, gboolean value);

/**
 * webkit_dom_html_input_element_get_checked:
 * @self: A #WebKitDOMHTMLInputElement
 *
 * Returns: A #gboolean
**/
WEBKIT_API gboolean
webkit_dom_html_input_element_get_checked(WebKitDOMHTMLInputElement* self);

/**
 * webkit_dom_html_input_element_set_checked:
 * @self: A #WebKitDOMHTMLInputElement
 * @value: A #gboolean
 *
**/
WEBKIT_API void
webkit_dom_html_input_element_set_checked(WebKitDOMHTMLInputElement* self, gboolean value);

/**
 * webkit_dom_html_input_element_get_dir_name:
 * @self: A #WebKitDOMHTMLInputElement
 *
 * Returns: A #gchar
**/
WEBKIT_API gchar*
webkit_dom_html_input_element_get_dir_name(WebKitDOMHTMLInputElement* self);

/**
 * webkit_dom_html_input_element_set_dir_name:
 * @self: A #WebKitDOMHTMLInputElement
 * @value: A #gchar
 *
**/
WEBKIT_API void
webkit_dom_html_input_element_set_dir_name(WebKitDOMHTMLInputElement* self, const gchar* value);

/**
 * webkit_dom_html_input_element_get_disabled:
 * @self: A #WebKitDOMHTMLInputElement
 *
 * Returns: A #gboolean
**/
WEBKIT_API gboolean
webkit_dom_html_input_element_get_disabled(WebKitDOMHTMLInputElement* self);

/**
 * webkit_dom_html_input_element_set_disabled:
 * @self: A #WebKitDOMHTMLInputElement
 * @value: A #gboolean
 *
**/
WEBKIT_API void
webkit_dom_html_input_element_set_disabled(WebKitDOMHTMLInputElement* self, gboolean value);

/**
 * webkit_dom_html_input_element_get_form:
 * @self: A #WebKitDOMHTMLInputElement
 *
 * Returns: (transfer none): A #WebKitDOMHTMLFormElement
**/
WEBKIT_API WebKitDOMHTMLFormElement*
webkit_dom_html_input_element_get_form(WebKitDOMHTMLInputElement* self);

/**
 * webkit_dom_html_input_element_get_files:
 * @self: A #WebKitDOMHTMLInputElement
 *
 * Returns: (transfer full): A #WebKitDOMFileList
**/
WEBKIT_API WebKitDOMFileList*
webkit_dom_html_input_element_get_files(WebKitDOMHTMLInputElement* self);

/**
 * webkit_dom_html_input_element_set_files:
 * @self: A #WebKitDOMHTMLInputElement
 * @value: A #WebKitDOMFileList
 *
**/
WEBKIT_API void
webkit_dom_html_input_element_set_files(WebKitDOMHTMLInputElement* self, WebKitDOMFileList* value);

/**
 * webkit_dom_html_input_element_get_form_action:
 * @self: A #WebKitDOMHTMLInputElement
 *
 * Returns: A #gchar
**/
WEBKIT_API gchar*
webkit_dom_html_input_element_get_form_action(WebKitDOMHTMLInputElement* self);

/**
 * webkit_dom_html_input_element_set_form_action:
 * @self: A #WebKitDOMHTMLInputElement
 * @value: A #gchar
 *
**/
WEBKIT_API void
webkit_dom_html_input_element_set_form_action(WebKitDOMHTMLInputElement* self, const gchar* value);

/**
 * webkit_dom_html_input_element_get_form_enctype:
 * @self: A #WebKitDOMHTMLInputElement
 *
 * Returns: A #gchar
**/
WEBKIT_API gchar*
webkit_dom_html_input_element_get_form_enctype(WebKitDOMHTMLInputElement* self);

/**
 * webkit_dom_html_input_element_set_form_enctype:
 * @self: A #WebKitDOMHTMLInputElement
 * @value: A #gchar
 *
**/
WEBKIT_API void
webkit_dom_html_input_element_set_form_enctype(WebKitDOMHTMLInputElement* self, const gchar* value);

/**
 * webkit_dom_html_input_element_get_form_method:
 * @self: A #WebKitDOMHTMLInputElement
 *
 * Returns: A #gchar
**/
WEBKIT_API gchar*
webkit_dom_html_input_element_get_form_method(WebKitDOMHTMLInputElement* self);

/**
 * webkit_dom_html_input_element_set_form_method:
 * @self: A #WebKitDOMHTMLInputElement
 * @value: A #gchar
 *
**/
WEBKIT_API void
webkit_dom_html_input_element_set_form_method(WebKitDOMHTMLInputElement* self, const gchar* value);

/**
 * webkit_dom_html_input_element_get_form_no_validate:
 * @self: A #WebKitDOMHTMLInputElement
 *
 * Returns: A #gboolean
**/
WEBKIT_API gboolean
webkit_dom_html_input_element_get_form_no_validate(WebKitDOMHTMLInputElement* self);

/**
 * webkit_dom_html_input_element_set_form_no_validate:
 * @self: A #WebKitDOMHTMLInputElement
 * @value: A #gboolean
 *
**/
WEBKIT_API void
webkit_dom_html_input_element_set_form_no_validate(WebKitDOMHTMLInputElement* self, gboolean value);

/**
 * webkit_dom_html_input_element_get_form_target:
 * @self: A #WebKitDOMHTMLInputElement
 *
 * Returns: A #gchar
**/
WEBKIT_API gchar*
webkit_dom_html_input_element_get_form_target(WebKitDOMHTMLInputElement* self);

/**
 * webkit_dom_html_input_element_set_form_target:
 * @self: A #WebKitDOMHTMLInputElement
 * @value: A #gchar
 *
**/
WEBKIT_API void
webkit_dom_html_input_element_set_form_target(WebKitDOMHTMLInputElement* self, const gchar* value);

/**
 * webkit_dom_html_input_element_get_height:
 * @self: A #WebKitDOMHTMLInputElement
 *
 * Returns: A #gulong
**/
WEBKIT_API gulong
webkit_dom_html_input_element_get_height(WebKitDOMHTMLInputElement* self);

/**
 * webkit_dom_html_input_element_set_height:
 * @self: A #WebKitDOMHTMLInputElement
 * @value: A #gulong
 *
**/
WEBKIT_API void
webkit_dom_html_input_element_set_height(WebKitDOMHTMLInputElement* self, gulong value);

/**
 * webkit_dom_html_input_element_get_indeterminate:
 * @self: A #WebKitDOMHTMLInputElement
 *
 * Returns: A #gboolean
**/
WEBKIT_API gboolean
webkit_dom_html_input_element_get_indeterminate(WebKitDOMHTMLInputElement* self);

/**
 * webkit_dom_html_input_element_set_indeterminate:
 * @self: A #WebKitDOMHTMLInputElement
 * @value: A #gboolean
 *
**/
WEBKIT_API void
webkit_dom_html_input_element_set_indeterminate(WebKitDOMHTMLInputElement* self, gboolean value);

/**
 * webkit_dom_html_input_element_get_list:
 * @self: A #WebKitDOMHTMLInputElement
 *
 * Returns: (transfer none): A #WebKitDOMHTMLElement
**/
WEBKIT_API WebKitDOMHTMLElement*
webkit_dom_html_input_element_get_list(WebKitDOMHTMLInputElement* self);

/**
 * webkit_dom_html_input_element_get_max:
 * @self: A #WebKitDOMHTMLInputElement
 *
 * Returns: A #gchar
**/
WEBKIT_API gchar*
webkit_dom_html_input_element_get_max(WebKitDOMHTMLInputElement* self);

/**
 * webkit_dom_html_input_element_set_max:
 * @self: A #WebKitDOMHTMLInputElement
 * @value: A #gchar
 *
**/
WEBKIT_API void
webkit_dom_html_input_element_set_max(WebKitDOMHTMLInputElement* self, const gchar* value);

/**
 * webkit_dom_html_input_element_get_max_length:
 * @self: A #WebKitDOMHTMLInputElement
 *
 * Returns: A #glong
**/
WEBKIT_API glong
webkit_dom_html_input_element_get_max_length(WebKitDOMHTMLInputElement* self);

/**
 * webkit_dom_html_input_element_set_max_length:
 * @self: A #WebKitDOMHTMLInputElement
 * @value: A #glong
 * @error: #GError
 *
**/
WEBKIT_API void
webkit_dom_html_input_element_set_max_length(WebKitDOMHTMLInputElement* self, glong value, GError** error);

/**
 * webkit_dom_html_input_element_get_min:
 * @self: A #WebKitDOMHTMLInputElement
 *
 * Returns: A #gchar
**/
WEBKIT_API gchar*
webkit_dom_html_input_element_get_min(WebKitDOMHTMLInputElement* self);

/**
 * webkit_dom_html_input_element_set_min:
 * @self: A #WebKitDOMHTMLInputElement
 * @value: A #gchar
 *
**/
WEBKIT_API void
webkit_dom_html_input_element_set_min(WebKitDOMHTMLInputElement* self, const gchar* value);

/**
 * webkit_dom_html_input_element_get_multiple:
 * @self: A #WebKitDOMHTMLInputElement
 *
 * Returns: A #gboolean
**/
WEBKIT_API gboolean
webkit_dom_html_input_element_get_multiple(WebKitDOMHTMLInputElement* self);

/**
 * webkit_dom_html_input_element_set_multiple:
 * @self: A #WebKitDOMHTMLInputElement
 * @value: A #gboolean
 *
**/
WEBKIT_API void
webkit_dom_html_input_element_set_multiple(WebKitDOMHTMLInputElement* self, gboolean value);

/**
 * webkit_dom_html_input_element_get_name:
 * @self: A #WebKitDOMHTMLInputElement
 *
 * Returns: A #gchar
**/
WEBKIT_API gchar*
webkit_dom_html_input_element_get_name(WebKitDOMHTMLInputElement* self);

/**
 * webkit_dom_html_input_element_set_name:
 * @self: A #WebKitDOMHTMLInputElement
 * @value: A #gchar
 *
**/
WEBKIT_API void
webkit_dom_html_input_element_set_name(WebKitDOMHTMLInputElement* self, const gchar* value);

/**
 * webkit_dom_html_input_element_get_pattern:
 * @self: A #WebKitDOMHTMLInputElement
 *
 * Returns: A #gchar
**/
WEBKIT_API gchar*
webkit_dom_html_input_element_get_pattern(WebKitDOMHTMLInputElement* self);

/**
 * webkit_dom_html_input_element_set_pattern:
 * @self: A #WebKitDOMHTMLInputElement
 * @value: A #gchar
 *
**/
WEBKIT_API void
webkit_dom_html_input_element_set_pattern(WebKitDOMHTMLInputElement* self, const gchar* value);

/**
 * webkit_dom_html_input_element_get_placeholder:
 * @self: A #WebKitDOMHTMLInputElement
 *
 * Returns: A #gchar
**/
WEBKIT_API gchar*
webkit_dom_html_input_element_get_placeholder(WebKitDOMHTMLInputElement* self);

/**
 * webkit_dom_html_input_element_set_placeholder:
 * @self: A #WebKitDOMHTMLInputElement
 * @value: A #gchar
 *
**/
WEBKIT_API void
webkit_dom_html_input_element_set_placeholder(WebKitDOMHTMLInputElement* self, const gchar* value);

/**
 * webkit_dom_html_input_element_get_read_only:
 * @self: A #WebKitDOMHTMLInputElement
 *
 * Returns: A #gboolean
**/
WEBKIT_API gboolean
webkit_dom_html_input_element_get_read_only(WebKitDOMHTMLInputElement* self);

/**
 * webkit_dom_html_input_element_set_read_only:
 * @self: A #WebKitDOMHTMLInputElement
 * @value: A #gboolean
 *
**/
WEBKIT_API void
webkit_dom_html_input_element_set_read_only(WebKitDOMHTMLInputElement* self, gboolean value);

/**
 * webkit_dom_html_input_element_get_required:
 * @self: A #WebKitDOMHTMLInputElement
 *
 * Returns: A #gboolean
**/
WEBKIT_API gboolean
webkit_dom_html_input_element_get_required(WebKitDOMHTMLInputElement* self);

/**
 * webkit_dom_html_input_element_set_required:
 * @self: A #WebKitDOMHTMLInputElement
 * @value: A #gboolean
 *
**/
WEBKIT_API void
webkit_dom_html_input_element_set_required(WebKitDOMHTMLInputElement* self, gboolean value);

/**
 * webkit_dom_html_input_element_get_size:
 * @self: A #WebKitDOMHTMLInputElement
 *
 * Returns: A #gulong
**/
WEBKIT_API gulong
webkit_dom_html_input_element_get_size(WebKitDOMHTMLInputElement* self);

/**
 * webkit_dom_html_input_element_set_size:
 * @self: A #WebKitDOMHTMLInputElement
 * @value: A #gulong
 * @error: #GError
 *
**/
WEBKIT_API void
webkit_dom_html_input_element_set_size(WebKitDOMHTMLInputElement* self, gulong value, GError** error);

/**
 * webkit_dom_html_input_element_get_src:
 * @self: A #WebKitDOMHTMLInputElement
 *
 * Returns: A #gchar
**/
WEBKIT_API gchar*
webkit_dom_html_input_element_get_src(WebKitDOMHTMLInputElement* self);

/**
 * webkit_dom_html_input_element_set_src:
 * @self: A #WebKitDOMHTMLInputElement
 * @value: A #gchar
 *
**/
WEBKIT_API void
webkit_dom_html_input_element_set_src(WebKitDOMHTMLInputElement* self, const gchar* value);

/**
 * webkit_dom_html_input_element_get_step:
 * @self: A #WebKitDOMHTMLInputElement
 *
 * Returns: A #gchar
**/
WEBKIT_API gchar*
webkit_dom_html_input_element_get_step(WebKitDOMHTMLInputElement* self);

/**
 * webkit_dom_html_input_element_set_step:
 * @self: A #WebKitDOMHTMLInputElement
 * @value: A #gchar
 *
**/
WEBKIT_API void
webkit_dom_html_input_element_set_step(WebKitDOMHTMLInputElement* self, const gchar* value);

/**
 * webkit_dom_html_input_element_get_default_value:
 * @self: A #WebKitDOMHTMLInputElement
 *
 * Returns: A #gchar
**/
WEBKIT_API gchar*
webkit_dom_html_input_element_get_default_value(WebKitDOMHTMLInputElement* self);

/**
 * webkit_dom_html_input_element_set_default_value:
 * @self: A #WebKitDOMHTMLInputElement
 * @value: A #gchar
 *
**/
WEBKIT_API void
webkit_dom_html_input_element_set_default_value(WebKitDOMHTMLInputElement* self, const gchar* value);

/**
 * webkit_dom_html_input_element_get_value:
 * @self: A #WebKitDOMHTMLInputElement
 *
 * Returns: A #gchar
**/
WEBKIT_API gchar*
webkit_dom_html_input_element_get_value(WebKitDOMHTMLInputElement* self);

/**
 * webkit_dom_html_input_element_set_value:
 * @self: A #WebKitDOMHTMLInputElement
 * @value: A #gchar
 *
**/
WEBKIT_API void
webkit_dom_html_input_element_set_value(WebKitDOMHTMLInputElement* self, const gchar* value);

/**
 * webkit_dom_html_input_element_get_value_as_number:
 * @self: A #WebKitDOMHTMLInputElement
 *
 * Returns: A #gdouble
**/
WEBKIT_API gdouble
webkit_dom_html_input_element_get_value_as_number(WebKitDOMHTMLInputElement* self);

/**
 * webkit_dom_html_input_element_set_value_as_number:
 * @self: A #WebKitDOMHTMLInputElement
 * @value: A #gdouble
 * @error: #GError
 *
**/
WEBKIT_API void
webkit_dom_html_input_element_set_value_as_number(WebKitDOMHTMLInputElement* self, gdouble value, GError** error);

/**
 * webkit_dom_html_input_element_get_width:
 * @self: A #WebKitDOMHTMLInputElement
 *
 * Returns: A #gulong
**/
WEBKIT_API gulong
webkit_dom_html_input_element_get_width(WebKitDOMHTMLInputElement* self);

/**
 * webkit_dom_html_input_element_set_width:
 * @self: A #WebKitDOMHTMLInputElement
 * @value: A #gulong
 *
**/
WEBKIT_API void
webkit_dom_html_input_element_set_width(WebKitDOMHTMLInputElement* self, gulong value);

/**
 * webkit_dom_html_input_element_get_will_validate:
 * @self: A #WebKitDOMHTMLInputElement
 *
 * Returns: A #gboolean
**/
WEBKIT_API gboolean
webkit_dom_html_input_element_get_will_validate(WebKitDOMHTMLInputElement* self);

/**
 * webkit_dom_html_input_element_get_validity:
 * @self: A #WebKitDOMHTMLInputElement
 *
 * Returns: (transfer full): A #WebKitDOMValidityState
**/
WEBKIT_API WebKitDOMValidityState*
webkit_dom_html_input_element_get_validity(WebKitDOMHTMLInputElement* self);

/**
 * webkit_dom_html_input_element_get_validation_message:
 * @self: A #WebKitDOMHTMLInputElement
 *
 * Returns: A #gchar
**/
WEBKIT_API gchar*
webkit_dom_html_input_element_get_validation_message(WebKitDOMHTMLInputElement* self);

/**
 * webkit_dom_html_input_element_get_labels:
 * @self: A #WebKitDOMHTMLInputElement
 *
 * Returns: (transfer full): A #WebKitDOMNodeList
**/
WEBKIT_API WebKitDOMNodeList*
webkit_dom_html_input_element_get_labels(WebKitDOMHTMLInputElement* self);

/**
 * webkit_dom_html_input_element_get_align:
 * @self: A #WebKitDOMHTMLInputElement
 *
 * Returns: A #gchar
**/
WEBKIT_API gchar*
webkit_dom_html_input_element_get_align(WebKitDOMHTMLInputElement* self);

/**
 * webkit_dom_html_input_element_set_align:
 * @self: A #WebKitDOMHTMLInputElement
 * @value: A #gchar
 *
**/
WEBKIT_API void
webkit_dom_html_input_element_set_align(WebKitDOMHTMLInputElement* self, const gchar* value);

/**
 * webkit_dom_html_input_element_get_webkitdirectory:
 * @self: A #WebKitDOMHTMLInputElement
 *
 * Returns: A #gboolean
**/
WEBKIT_API gboolean
webkit_dom_html_input_element_get_webkitdirectory(WebKitDOMHTMLInputElement* self);

/**
 * webkit_dom_html_input_element_set_webkitdirectory:
 * @self: A #WebKitDOMHTMLInputElement
 * @value: A #gboolean
 *
**/
WEBKIT_API void
webkit_dom_html_input_element_set_webkitdirectory(WebKitDOMHTMLInputElement* self, gboolean value);

/**
 * webkit_dom_html_input_element_get_use_map:
 * @self: A #WebKitDOMHTMLInputElement
 *
 * Returns: A #gchar
**/
WEBKIT_API gchar*
webkit_dom_html_input_element_get_use_map(WebKitDOMHTMLInputElement* self);

/**
 * webkit_dom_html_input_element_set_use_map:
 * @self: A #WebKitDOMHTMLInputElement
 * @value: A #gchar
 *
**/
WEBKIT_API void
webkit_dom_html_input_element_set_use_map(WebKitDOMHTMLInputElement* self, const gchar* value);

/**
 * webkit_dom_html_input_element_get_incremental:
 * @self: A #WebKitDOMHTMLInputElement
 *
 * Returns: A #gboolean
**/
WEBKIT_API gboolean
webkit_dom_html_input_element_get_incremental(WebKitDOMHTMLInputElement* self);

/**
 * webkit_dom_html_input_element_set_incremental:
 * @self: A #WebKitDOMHTMLInputElement
 * @value: A #gboolean
 *
**/
WEBKIT_API void
webkit_dom_html_input_element_set_incremental(WebKitDOMHTMLInputElement* self, gboolean value);

/**
 * webkit_dom_html_input_element_get_webkit_speech:
 * @self: A #WebKitDOMHTMLInputElement
 *
 * Returns: A #gboolean
**/
WEBKIT_API gboolean
webkit_dom_html_input_element_get_webkit_speech(WebKitDOMHTMLInputElement* self);

/**
 * webkit_dom_html_input_element_set_webkit_speech:
 * @self: A #WebKitDOMHTMLInputElement
 * @value: A #gboolean
 *
**/
WEBKIT_API void
webkit_dom_html_input_element_set_webkit_speech(WebKitDOMHTMLInputElement* self, gboolean value);

/**
 * webkit_dom_html_input_element_get_webkit_grammar:
 * @self: A #WebKitDOMHTMLInputElement
 *
 * Returns: A #gboolean
**/
WEBKIT_API gboolean
webkit_dom_html_input_element_get_webkit_grammar(WebKitDOMHTMLInputElement* self);

/**
 * webkit_dom_html_input_element_set_webkit_grammar:
 * @self: A #WebKitDOMHTMLInputElement
 * @value: A #gboolean
 *
**/
WEBKIT_API void
webkit_dom_html_input_element_set_webkit_grammar(WebKitDOMHTMLInputElement* self, gboolean value);

/**
 * webkit_dom_html_input_element_get_autocorrect:
 * @self: A #WebKitDOMHTMLInputElement
 *
 * Returns: A #gboolean
**/
WEBKIT_API gboolean
webkit_dom_html_input_element_get_autocorrect(WebKitDOMHTMLInputElement* self);

/**
 * webkit_dom_html_input_element_set_autocorrect:
 * @self: A #WebKitDOMHTMLInputElement
 * @value: A #gboolean
 *
**/
WEBKIT_API void
webkit_dom_html_input_element_set_autocorrect(WebKitDOMHTMLInputElement* self, gboolean value);

/**
 * webkit_dom_html_input_element_get_autocapitalize:
 * @self: A #WebKitDOMHTMLInputElement
 *
 * Returns: A #gchar
**/
WEBKIT_API gchar*
webkit_dom_html_input_element_get_autocapitalize(WebKitDOMHTMLInputElement* self);

/**
 * webkit_dom_html_input_element_set_autocapitalize:
 * @self: A #WebKitDOMHTMLInputElement
 * @value: A #gchar
 *
**/
WEBKIT_API void
webkit_dom_html_input_element_set_autocapitalize(WebKitDOMHTMLInputElement* self, const gchar* value);

/**
 * webkit_dom_html_input_element_get_capture:
 * @self: A #WebKitDOMHTMLInputElement
 *
 * Returns: A #gchar
**/
WEBKIT_API gchar*
webkit_dom_html_input_element_get_capture(WebKitDOMHTMLInputElement* self);

/**
 * webkit_dom_html_input_element_set_capture:
 * @self: A #WebKitDOMHTMLInputElement
 * @value: A #gchar
 *
**/
WEBKIT_API void
webkit_dom_html_input_element_set_capture(WebKitDOMHTMLInputElement* self, const gchar* value);

G_END_DECLS

#endif /* WebKitDOMHTMLInputElement_h */