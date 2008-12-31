/*
 *  Copyright (C) 2008 Michal Hruby <michal.mhr@gmail.com>
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this library; if not, write to the
 * Free Software Foundation, Inc., 59 Temple Place - Suite 330,
 * Boston, MA 02111-1307, USA.
 */

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include "awn-effect-simple.h"

#include <math.h>
#include <string.h>
#include <stdlib.h>

gboolean
simple_hover_effect(AwnEffectsAnimation * anim)
{
  AwnEffectsPrivate *priv = anim->effects->priv;

  AWN_ANIMATION_INIT(anim) {
    priv->glow_amount = 1.0;
  }

  // repaint widget
  awn_effects_redraw(anim->effects);

  if (awn_effect_check_top_effect(anim, NULL))
    return awn_effect_suspend_animation(anim,
                                        (GSourceFunc)simple_hover_effect);
  else
    priv->glow_amount = 0.0;

  // check for repeating, but it'll return FALSE anyway if we're here
  gboolean repeat = awn_effect_handle_repeating(anim);

  return repeat;
}

gboolean
simple_attention_effect(AwnEffectsAnimation * anim)
{
  AwnEffectsPrivate *priv = anim->effects->priv;

  AWN_ANIMATION_INIT(anim) {
    priv->simple_rect = TRUE;
  }

  // repaint widget
  awn_effects_redraw(anim->effects);

  if (awn_effect_check_top_effect(anim, NULL))
    return awn_effect_suspend_animation(anim,
                                        (GSourceFunc)simple_attention_effect);
  else
    priv->simple_rect = FALSE;

  // check for repeating, but it'll return FALSE anyway if we're here
  gboolean repeat = awn_effect_handle_repeating(anim);

  return repeat;
}
