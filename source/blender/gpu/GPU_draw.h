/*
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; either version 2
 * of the License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software Foundation,
 * Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
 *
 * The Original Code is Copyright (C) 2005 Blender Foundation.
 * All rights reserved.
 */

/** \file
 * \ingroup gpu
 */

#ifndef __GPU_DRAW_H__
#define __GPU_DRAW_H__

#include "BLI_utildefines.h"

#ifdef __cplusplus
extern "C" {
#endif

struct FluidModifierData;

/* Fluid simulation.  */
void GPU_create_smoke(struct FluidModifierData *fmd, int highres);
void GPU_create_smoke_coba_field(struct FluidModifierData *fmd);
void GPU_create_smoke_velocity(struct FluidModifierData *fmd);

/* Image updates and free. */
void GPU_free_smoke(struct FluidModifierData *fmd);
void GPU_free_smoke_velocity(struct FluidModifierData *fmd);

#ifdef __cplusplus
}
#endif

#endif
