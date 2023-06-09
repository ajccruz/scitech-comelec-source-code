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

#ifndef WebKitDOMMediaController_h
#define WebKitDOMMediaController_h

#include <glib-object.h>
#include <webkitdom/WebKitDOMObject.h>
#include <webkitdom/webkitdomdefines.h>

G_BEGIN_DECLS

#define WEBKIT_TYPE_DOM_MEDIA_CONTROLLER            (webkit_dom_media_controller_get_type())
#define WEBKIT_DOM_MEDIA_CONTROLLER(obj)            (G_TYPE_CHECK_INSTANCE_CAST((obj), WEBKIT_TYPE_DOM_MEDIA_CONTROLLER, WebKitDOMMediaController))
#define WEBKIT_DOM_MEDIA_CONTROLLER_CLASS(klass)    (G_TYPE_CHECK_CLASS_CAST((klass),  WEBKIT_TYPE_DOM_MEDIA_CONTROLLER, WebKitDOMMediaControllerClass)
#define WEBKIT_DOM_IS_MEDIA_CONTROLLER(obj)         (G_TYPE_CHECK_INSTANCE_TYPE((obj), WEBKIT_TYPE_DOM_MEDIA_CONTROLLER))
#define WEBKIT_DOM_IS_MEDIA_CONTROLLER_CLASS(klass) (G_TYPE_CHECK_CLASS_TYPE((klass),  WEBKIT_TYPE_DOM_MEDIA_CONTROLLER))
#define WEBKIT_DOM_MEDIA_CONTROLLER_GET_CLASS(obj)  (G_TYPE_INSTANCE_GET_CLASS((obj),  WEBKIT_TYPE_DOM_MEDIA_CONTROLLER, WebKitDOMMediaControllerClass))

struct _WebKitDOMMediaController {
    WebKitDOMObject parent_instance;
};

struct _WebKitDOMMediaControllerClass {
    WebKitDOMObjectClass parent_class;
};

WEBKIT_API GType
webkit_dom_media_controller_get_type (void);

/**
 * webkit_dom_media_controller_play:
 * @self: A #WebKitDOMMediaController
 *
**/
WEBKIT_API void
webkit_dom_media_controller_play(WebKitDOMMediaController* self);

/**
 * webkit_dom_media_controller_pause:
 * @self: A #WebKitDOMMediaController
 *
**/
WEBKIT_API void
webkit_dom_media_controller_pause(WebKitDOMMediaController* self);

/**
 * webkit_dom_media_controller_unpause:
 * @self: A #WebKitDOMMediaController
 *
**/
WEBKIT_API void
webkit_dom_media_controller_unpause(WebKitDOMMediaController* self);

/**
 * webkit_dom_media_controller_get_buffered:
 * @self: A #WebKitDOMMediaController
 *
 * Returns: (transfer full): A #WebKitDOMTimeRanges
**/
WEBKIT_API WebKitDOMTimeRanges*
webkit_dom_media_controller_get_buffered(WebKitDOMMediaController* self);

/**
 * webkit_dom_media_controller_get_seekable:
 * @self: A #WebKitDOMMediaController
 *
 * Returns: (transfer full): A #WebKitDOMTimeRanges
**/
WEBKIT_API WebKitDOMTimeRanges*
webkit_dom_media_controller_get_seekable(WebKitDOMMediaController* self);

/**
 * webkit_dom_media_controller_get_duration:
 * @self: A #WebKitDOMMediaController
 *
 * Returns: A #gdouble
**/
WEBKIT_API gdouble
webkit_dom_media_controller_get_duration(WebKitDOMMediaController* self);

/**
 * webkit_dom_media_controller_get_current_time:
 * @self: A #WebKitDOMMediaController
 *
 * Returns: A #gdouble
**/
WEBKIT_API gdouble
webkit_dom_media_controller_get_current_time(WebKitDOMMediaController* self);

/**
 * webkit_dom_media_controller_set_current_time:
 * @self: A #WebKitDOMMediaController
 * @value: A #gdouble
 *
**/
WEBKIT_API void
webkit_dom_media_controller_set_current_time(WebKitDOMMediaController* self, gdouble value);

/**
 * webkit_dom_media_controller_get_paused:
 * @self: A #WebKitDOMMediaController
 *
 * Returns: A #gboolean
**/
WEBKIT_API gboolean
webkit_dom_media_controller_get_paused(WebKitDOMMediaController* self);

/**
 * webkit_dom_media_controller_get_played:
 * @self: A #WebKitDOMMediaController
 *
 * Returns: (transfer full): A #WebKitDOMTimeRanges
**/
WEBKIT_API WebKitDOMTimeRanges*
webkit_dom_media_controller_get_played(WebKitDOMMediaController* self);

/**
 * webkit_dom_media_controller_get_playback_state:
 * @self: A #WebKitDOMMediaController
 *
 * Returns: A #gchar
**/
WEBKIT_API gchar*
webkit_dom_media_controller_get_playback_state(WebKitDOMMediaController* self);

/**
 * webkit_dom_media_controller_get_default_playback_rate:
 * @self: A #WebKitDOMMediaController
 *
 * Returns: A #gdouble
**/
WEBKIT_API gdouble
webkit_dom_media_controller_get_default_playback_rate(WebKitDOMMediaController* self);

/**
 * webkit_dom_media_controller_set_default_playback_rate:
 * @self: A #WebKitDOMMediaController
 * @value: A #gdouble
 *
**/
WEBKIT_API void
webkit_dom_media_controller_set_default_playback_rate(WebKitDOMMediaController* self, gdouble value);

/**
 * webkit_dom_media_controller_get_playback_rate:
 * @self: A #WebKitDOMMediaController
 *
 * Returns: A #gdouble
**/
WEBKIT_API gdouble
webkit_dom_media_controller_get_playback_rate(WebKitDOMMediaController* self);

/**
 * webkit_dom_media_controller_set_playback_rate:
 * @self: A #WebKitDOMMediaController
 * @value: A #gdouble
 *
**/
WEBKIT_API void
webkit_dom_media_controller_set_playback_rate(WebKitDOMMediaController* self, gdouble value);

/**
 * webkit_dom_media_controller_get_volume:
 * @self: A #WebKitDOMMediaController
 *
 * Returns: A #gdouble
**/
WEBKIT_API gdouble
webkit_dom_media_controller_get_volume(WebKitDOMMediaController* self);

/**
 * webkit_dom_media_controller_set_volume:
 * @self: A #WebKitDOMMediaController
 * @value: A #gdouble
 * @error: #GError
 *
**/
WEBKIT_API void
webkit_dom_media_controller_set_volume(WebKitDOMMediaController* self, gdouble value, GError** error);

/**
 * webkit_dom_media_controller_get_muted:
 * @self: A #WebKitDOMMediaController
 *
 * Returns: A #gboolean
**/
WEBKIT_API gboolean
webkit_dom_media_controller_get_muted(WebKitDOMMediaController* self);

/**
 * webkit_dom_media_controller_set_muted:
 * @self: A #WebKitDOMMediaController
 * @value: A #gboolean
 *
**/
WEBKIT_API void
webkit_dom_media_controller_set_muted(WebKitDOMMediaController* self, gboolean value);

G_END_DECLS

#endif /* WebKitDOMMediaController_h */
