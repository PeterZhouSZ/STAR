# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Max-Planck-Gesellschaft zur Förderung der Wissenschaften e.V. (MPG),
# acting on behalf of its Max Planck Institute for Intelligent Systems and the
# Max Planck Institute for Biological Cybernetics. All rights reserved.
#
# Max-Planck-Gesellschaft zur Förderung der Wissenschaften e.V. (MPG) is holder of all proprietary rights
# on this computer program. You can only use this computer program if you have closed a license agreement
# with MPG or you get the right to use the computer program from someone who is authorized to grant you that right.
# Any use of the computer program without a valid license is prohibited and liable to prosecution.
# Contact: ps-license@tuebingen.mpg.de
#
#
# If you use this code in a research publication please consider citing the following:
#
# STAR: Sparse Trained  Articulated Human Body Regressor <https://arxiv.org/pdf/2008.08535.pdf>
#
#
# Code Developed by:
# Ahmed A. A. Osman 

import chumpy  as ch
import numpy as np
import os
from .verts import verts_decorated_quat 
from config import cfg 

def load_model(gender='female',num_betas=10):
    if gender not in ['male','female']:
        raise RuntimeError('Invalid model gender!')
    fname = os.path.join(cfg.path_star,gender,'model.npy')
    model_dict  = np.load(fname,allow_pickle=True,encoding='latin1')[()]
    trans       = ch.array(np.zeros(3))
    posedirs    = ch.array(model_dict['posedirs'])
    v_tempalate = ch.array(model_dict['v_template'])

    J_regressor   = model_dict['J_regressor'] #Regressor of the model
    weights       = ch.array(model_dict['weights']) #Weights
    num_joints    = weights.shape[1]
    kintree_table = model_dict['kintree_table']
    f = model_dict['f']

    betas = ch.array(np.zeros((model_dict['shapedirs'].shape[-1]))) #Betas
    shapedirs = ch.array(model_dict['shapedirs']) #Shape Corrective Blend shapes
    pose = ch.array(np.zeros((num_joints*3))) #Pose Angles

    model = verts_decorated_quat(trans=trans,
                    pose=pose,
                    v_template=v_tempalate,
                    J=J_regressor,
                    weights=weights,
                    kintree_table=kintree_table,
                    f=f,
                    posedirs=posedirs,
                    betas=betas,
                    shapedirs=shapedirs,
                    want_Jtr=True)
    return model