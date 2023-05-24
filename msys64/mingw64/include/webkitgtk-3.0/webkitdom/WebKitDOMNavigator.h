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

#ifndef WebKitDOMNavigator_h
#define WebKitDOMNavigator_h

#include <glib-object.h>
#include <webkitdom/WebKitDOMObject.h>
#include <webkitdom/webkitdomdefines.h>

G_BEGIN_DECLS

#define WEBKIT_TYPE_DOM_NAVIGATOR            (webkit_dom_navigator_get_type())
#define WEBKIT_DOM_NAVIGATOR(obj)            (G_TYPE_CHECK_INSTANCE_CAST((obj), WEBKIT_TYPE_DOM_NAVIGATOR, WebKitDOMNavigator))
#define WEBKIT_DOM_NAVIGATOR_CLASS(klass)    (G_TYPE_CHECK_CLASS_CAST((klass),  WEBKIT_TYPE_DOM_NAVIGATOR, WebKitDOMNavigatorClass)
#define WEBKIT_DOM_IS_NAVIGATOR(obj)         (G_TYPE_CHECK_INSTANCE_TYPE((obj), WEBKIT_TYPE_DOM_NAVIGATOR))
#define WEBKIT_DOM_IS_NAVIGATOR_CLASS(klass) (G_TYPE_CHECK_CLASS_TYPE((klass),  WEBKIT_TYPE_DOM_NAVIGATOR))
#define WEBKIT_DOM_NAVIGATOR_GET_CLASS(obj)  (G_TYPE_INSTANCE_GET_CLASS((obj),  WEBKIT_TYPE_DOM_NAVIGATOR, WebKitDOMNavigatorClass))

struct _WebKitDOMNavigator {
    WebKitDOMObject parent_instance;
};

struct _WebKitDOMNavigatorClass {
    WebKitDOMObjectClass parent_class;
};

WEBKIT_API GType
webkit_dom_navigator_get_type (void);

/**
 * webkit_dom_navigator_java_enabled:
 * @self: A #WebKitDOMNavigator
 *
 * Returns: A #gboolean
**/
WEBKIT_API gboolean
webkit_dom_navigator_java_enabled(WebKitDOMNavigator* self);

/**
 * webkit_dom_navigator_get_storage_updates:
 * @self: A #WebKitDOMNavigator
 *
**/
WEBKIT_API void
webkit_dom_navigator_get_storage_updates(WebKitDOMNavigator* self);

/**
 * webkit_dom_navigator_webkit_get_gamepads:
 * @self: A #WebKitDOMNavigator
 *
 * Returns: (transfer full): A #WebKitDOMGamepadList
**/
WEBKIT_API WebKitDOMGamepadList*
webkit_dom_navigator_webkit_get_gamepads(WebKitDOMNavigator* self);

/**
 * webkit_dom_navigator_register_protocol_handler:
 * @self: A #WebKitDOMNavigator
 * @scheme: A #gchar
 * @url: A #gchar
 * @title: A #gchar
 * @error: #GError
 *
**/
WEBKIT_API void
webkit_dom_navigator_register_protocol_handler(WebKitDOMNavigator* self, const gchar* scheme, const gchar* url, const gchar* title, GError** error);

/**
 * webkit_dom_navigator_is_protocol_handler_registered:
 * @self: A #WebKitDOMNavigator
 * @scheme: A #gchar
 * @url: A #gchar
 * @error: #GError
 *
 * Returns: A #gchar
**/
WEBKIT_API gchar*
webkit_dom_navigator_is_protocol_handler_registered(WebKitDOMNavigator* self, const gchar* scheme, const gchar* url, GError** error);

/**
 * webkit_dom_navigator_unregister_protocol_handler:
 * @self: A #WebKitDOMNavigator
 * @scheme: A #gchar
 * @url: A #gchar
 * @error: #GError
 *
**/
WEBKIT_API void
webkit_dom_navigator_unregister_protocol_handler(WebKitDOMNavigator* self, const gchar* scheme, const gchar* url, GError** error);

/**
 * webkit_dom_navigator_get_app_code_name:
 * @self: A #WebKitDOMNavigator
 *
 * Returns: A #gchar
**/
WEBKIT_API gchar*
webkit_dom_navigator_get_app_code_name(WebKitDOMNavigator* self);

/**
 * webkit_dom_navigator_get_app_name:
 * @self: A #WebKitDOMNavigator
 *
 * Returns: A #gchar
**/
WEBKIT_API gchar*
webkit_dom_navigator_get_app_name(WebKitDOMNavigator* self);

/**
 * webkit_dom_navigator_get_app_version:
 * @self: A #WebKitDOMNavigator
 *
 * Returns: A #gchar
**/
WEBKIT_API gchar*
webkit_dom_navigator_get_app_version(WebKitDOMNavigator* self);

/**
 * webkit_dom_navigator_get_language:
 * @self: A #WebKitDOMNavigator
 *
 * Returns: A #gchar
**/
WEBKIT_API gchar*
webkit_dom_navigator_get_language(WebKitDOMNavigator* self);

/**
 * webkit_dom_navigator_get_user_agent:
 * @self: A #WebKitDOMNavigator
 *
 * Returns: A #gchar
**/
WEBKIT_API gchar*
webkit_dom_navigator_get_user_agent(WebKitDOMNavigator* self);

/**
 * webkit_dom_navigator_get_platform:
 * @self: A #WebKitDOMNavigator
 *
 * Returns: A #gchar
**/
WEBKIT_API gchar*
webkit_dom_navigator_get_platform(WebKitDOMNavigator* self);

/**
 * webkit_dom_navigator_get_plugins:
 * @self: A #WebKitDOMNavigator
 *
 * Returns: (transfer full): A #WebKitDOMDOMPluginArray
**/
WEBKIT_API WebKitDOMDOMPluginArray*
webkit_dom_navigator_get_plugins(WebKitDOMNavigator* self);

/**
 * webkit_dom_navigator_get_mime_types:
 * @self: A #WebKitDOMNavigator
 *
 * Returns: (transfer full): A #WebKitDOMDOMMimeTypeArray
**/
WEBKIT_API WebKitDOMDOMMimeTypeArray*
webkit_dom_navigator_get_mime_types(WebKitDOMNavigator* self);

/**
 * webkit_dom_navigator_get_product:
 * @self: A #WebKitDOMNavigator
 *
 * Returns: A #gchar
**/
WEBKIT_API gchar*
webkit_dom_navigator_get_product(WebKitDOMNavigator* self);

/**
 * webkit_dom_navigator_get_product_sub:
 * @self: A #WebKitDOMNavigator
 *
 * Returns: A #gchar
**/
WEBKIT_API gchar*
webkit_dom_navigator_get_product_sub(WebKitDOMNavigator* self);

/**
 * webkit_dom_navigator_get_vendor:
 * @self: A #WebKitDOMNavigator
 *
 * Returns: A #gchar
**/
WEBKIT_API gchar*
webkit_dom_navigator_get_vendor(WebKitDOMNavigator* self);

/**
 * webkit_dom_navigator_get_vendor_sub:
 * @self: A #WebKitDOMNavigator
 *
 * Returns: A #gchar
**/
WEBKIT_API gchar*
webkit_dom_navigator_get_vendor_sub(WebKitDOMNavigator* self);

/**
 * webkit_dom_navigator_get_cookie_enabled:
 * @self: A #WebKitDOMNavigator
 *
 * Returns: A #gboolean
**/
WEBKIT_API gboolean
webkit_dom_navigator_get_cookie_enabled(WebKitDOMNavigator* self);

/**
 * webkit_dom_navigator_get_on_line:
 * @self: A #WebKitDOMNavigator
 *
 * Returns: A #gboolean
**/
WEBKIT_API gboolean
webkit_dom_navigator_get_on_line(WebKitDOMNavigator* self);

/**
 * webkit_dom_navigator_get_webkit_battery:
 * @self: A #WebKitDOMNavigator
 *
 * Returns: (transfer full): A #WebKitDOMBatteryManager
**/
WEBKIT_API WebKitDOMBatteryManager*
webkit_dom_navigator_get_webkit_battery(WebKitDOMNavigator* self);

/**
 * webkit_dom_navigator_get_geolocation:
 * @self: A #WebKitDOMNavigator
 *
 * Returns: (transfer full): A #WebKitDOMGeolocation
**/
WEBKIT_API WebKitDOMGeolocation*
webkit_dom_navigator_get_geolocation(WebKitDOMNavigator* self);

/**
 * webkit_dom_navigator_get_webkit_temporary_storage:
 * @self: A #WebKitDOMNavigator
 *
 * Returns: (transfer none): A #WebKitDOMStorageQuota
**/
WEBKIT_API WebKitDOMStorageQuota*
webkit_dom_navigator_get_webkit_temporary_storage(WebKitDOMNavigator* self);

/**
 * webkit_dom_navigator_get_webkit_persistent_storage:
 * @self: A #WebKitDOMNavigator
 *
 * Returns: (transfer none): A #WebKitDOMStorageQuota
**/
WEBKIT_API WebKitDOMStorageQuota*
webkit_dom_navigator_get_webkit_persistent_storage(WebKitDOMNavigator* self);

G_END_DECLS

#endif /* WebKitDOMNavigator_h */