from Tools.Weights.Weights import Weight

lumi = Weight("(41.529)",[])

weight = Weight("weight",["weight"])
zvtx_electron = Weight("0.991",[])

semilep = Weight("sf_SingleXorCrossTrigger",["sf_SingleXorCrossTrigger"])
had = Weight("sf_DoubleTauTight",["sf_DoubleTauTight"])

tauidsft_1 = Weight("( 0.89*(gen_match_1 == 5) + 1.0*(gen_match_1 !=5) )",["gen_match_1"])
tauidsft_2 = Weight("( 0.89*(gen_match_2 == 5) + 1.0*(gen_match_2 !=5) )",["gen_match_2"])

tauidsft = tauidsft_1 * tauidsft_2

zptweight = Weight("zPtReweightWeight",["zPtReweightWeight"])
topweight = Weight("topPtReweightWeightRun1", ["topPtReweightWeightRun1"])
prefire = Weight( "( ( 0.95+0.02*( (jpt_1>0 & jpt_1<200) & (njets<2 | ( (jdeta<2.8 | mjj<400 ) & (mjj<60 | mjj>=120 ) ) ) ) - 0.1*(jpt_1>=200) ) ) ", ["jpt_1","njets","jdeta","mjj"] )
ggh_nnlo = Weight("NNLO_ggH_weight",["NNLO_ggH_weight"])



signals_ggh = ["ggH125",
           "ggH_VBFTOPO_JET3VETO125",
           "ggH_VBFTOPO_JET3125",
           "ggH_0J125",
           "ggH_1J_PTH_0_60125",
           "ggH_1J_PTH_60_120125",
           "ggH_1J_PTH_120_200125",
           "ggH_1J_PTH_GT200125",
           "ggH_GE2J_PTH_0_60125",
           "ggH_GE2J_PTH_60_120125",
           "ggH_GE2J_PTH_120_200125",
           "ggH_GE2J_PTH_GT200125"
            ]
signals_qqh = ["qqH125",
                "qqH_VBFTOPO_JET3VETO125", "qqH_VBFTOPO_JET3125", "qqH_REST125",
                "qqH_PTJET1_GT200125", "qqH_VH2JET125"]

signals_VH = ["WH125","ZH125"]

signals = signals_ggh + signals_qqh + signals_VH

config = {

    "template_weight":{
        "mt":{
            "Z":      lumi  * weight * semilep * tauidsft_2 * zptweight,
            "W":      lumi  * weight * semilep * tauidsft_2,
            "TT":     lumi * weight * semilep * tauidsft_2 * topweight,
            "VV":     lumi * weight * semilep * tauidsft_2,
            "EMB":    weight,
            "ggH125": lumi * weight * semilep * tauidsft_2 * ggh_nnlo,
            "qqH125": lumi * weight * semilep * tauidsft_2 * prefire,
            "WH125":  lumi * weight * semilep * tauidsft_2,
            "ZH125":  lumi * weight * semilep * tauidsft_2,
            "ttH125": lumi * weight * semilep * tauidsft_2,
            "qqHWW":  lumi * weight * semilep * tauidsft_2,
            "ggHWW":  lumi * weight * semilep * tauidsft_2
        },
        "et":{
            # "Z":      lumi * kit_dy_stitching * weight * zvtx_electron * semilep * tauidsft_2 * zptweight,
            "Z":      lumi  * weight * zvtx_electron * semilep * tauidsft_2 * zptweight,
            "W":      lumi  * weight * zvtx_electron * semilep * tauidsft_2,
            "TT":     lumi * weight * zvtx_electron * semilep * tauidsft_2 * topweight,
            "VV":     lumi * weight * zvtx_electron * semilep * tauidsft_2,
            "EMB":    weight,
            "ggH125": lumi * weight * zvtx_electron * semilep * tauidsft_2 + ggh_nnlo,
            "qqH125": lumi * weight * zvtx_electron * semilep * tauidsft_2 * prefire,
            "WH125":  lumi * weight * zvtx_electron * semilep * tauidsft_2,
            "ZH125":  lumi * weight * zvtx_electron * semilep * tauidsft_2,
            "ttH125": lumi * weight * zvtx_electron * semilep * tauidsft_2,
            "qqHWW":  lumi * weight * zvtx_electron * semilep * tauidsft_2,
            "ggHWW":  lumi * weight * zvtx_electron * semilep * tauidsft_2
        },
        "tt":{
            "Z":      lumi  * weight * had * tauidsft * zptweight,
            "W":      lumi  * weight * had * tauidsft,
            "TT":     lumi * weight * had * tauidsft * topweight,
            "VV":     lumi * weight * had * tauidsft,
            "EMB":    weight,
            "ggH125": lumi * weight * had * tauidsft + ggh_nnlo,
            "qqH125": lumi * weight * had * tauidsft * prefire,
            "WH125":  lumi * weight * had * tauidsft,
            "ZH125":  lumi * weight * had * tauidsft,
            "ttH125": lumi * weight * had * tauidsft,
            "qqHWW":  lumi * weight * had * tauidsft,
            "ggHWW":  lumi * weight * had * tauidsft
        }
    },
    "reweighting":{
        "general":{
            "apply_to":["all"],
            "weights":{
                "CMS_scale_met_unclusteredUp"           : Weight("",[]),
                "CMS_scale_met_unclusteredDown"         : Weight("",[])
            }
        },
        "ttbar_all":{
            "apply_to":["TT","TTT","TTJ","TTL"],
            "weights":{
                "CMS_htt_ttbarShapeUp"                          : Weight("topPtReweightWeightRun1",["topPtReweightWeightRun1"]),
                "CMS_htt_ttbarShapeDown"                        : Weight("1.0 / topPtReweightWeightRun1",["topPtReweightWeightRun1"]),
            }
        },
        "dy_all":{
            "apply_to":["Z","ZTT","ZJ","ZL"],
            "weights":{
                "CMS_htt_dyShape_Run2017Up"                             : Weight("zPtReweightWeight",["zPtReweightWeight"]),
                "CMS_htt_dyShape_Run2017Down"                           : Weight("1.0 / zPtReweightWeight",["zPtReweightWeight"]),
            }
        },
        "embedding_uncertainties":{
            "apply_to":["EMB"],
            "weights":{
                "CMS_3ProngEffUp"                               : Weight("(embeddedDecayModeWeight_effUp_pi0Nom   / embeddedDecayModeWeight)", ["embeddedDecayModeWeight","embeddedDecayModeWeight_effUp_pi0Nom"] ),
                "CMS_3ProngEffDown"                             : Weight("(embeddedDecayModeWeight_effDown_pi0Nom / embeddedDecayModeWeight)", ["embeddedDecayModeWeight","embeddedDecayModeWeight_effDown_pi0Nom"] ),
                "CMS_1ProngPi0EffUp"                            : Weight("(embeddedDecayModeWeight_effNom_pi0Up   / embeddedDecayModeWeight)", ["embeddedDecayModeWeight","embeddedDecayModeWeight_effNom_pi0Up"] ),
                "CMS_1ProngPi0EffDown"                          : Weight("(embeddedDecayModeWeight_effNom_pi0Down / embeddedDecayModeWeight)", ["embeddedDecayModeWeight","embeddedDecayModeWeight_effNom_pi0Down"] ),
                "CMS_3ProngEff_Run2017Up"                       : Weight("(embeddedDecayModeWeight_effUp_pi0Nom   / embeddedDecayModeWeight)", ["embeddedDecayModeWeight","embeddedDecayModeWeight_effUp_pi0Nom"] ),
                "CMS_3ProngEff_Run2017Down"                     : Weight("(embeddedDecayModeWeight_effDown_pi0Nom / embeddedDecayModeWeight)", ["embeddedDecayModeWeight","embeddedDecayModeWeight_effDown_pi0Nom"] ),
                "CMS_1ProngPi0Eff_Run2017Up"                    : Weight("(embeddedDecayModeWeight_effNom_pi0Up   / embeddedDecayModeWeight)", ["embeddedDecayModeWeight","embeddedDecayModeWeight_effNom_pi0Up"] ),
                "CMS_1ProngPi0Eff_Run2017Down"                  : Weight("(embeddedDecayModeWeight_effNom_pi0Down / embeddedDecayModeWeight)", ["embeddedDecayModeWeight","embeddedDecayModeWeight_effNom_pi0Down"] )                
            }
        },        
        "genuine_taus":{
            "apply_to":["ZTT","TTT","VVT","TTL","VVL","ZL","EMB","ggH125","qqH125"],
            "weights":{
                "CMS_scale_t_1prong_Run2017Up"                : Weight("",[]),
                "CMS_scale_t_1prong_Run2017Down"              : Weight("",[]),
                "CMS_scale_t_1prong1pizero_Run2017Up"         : Weight("",[]),
                "CMS_scale_t_1prong1pizero_Run2017Down"       : Weight("",[]),
                "CMS_scale_t_3prong_Run2017Up"                : Weight("",[]),
                "CMS_scale_t_3prong_Run2017Down"              : Weight("",[])
            }
        },
        "jet_fakes":{
            "apply_to":["ZJ","TTJ","VVJ","W"],
            "weights":{
                "CMS_htt_jetToTauFake_Run2017Up"              :{
                    "et":Weight("((1-0.002*pt_2)*(pt_2 < 200) + 0.6*(pt_2 >= 200))", ["pt_2"]),
                    "mt":Weight("((1-0.002*pt_2)*(pt_2 < 200) + 0.6*(pt_2 >= 200))", ["pt_2"]),
                    "tt":Weight("(( (1-0.002*pt_1)*(pt_1 < 200) + 0.6*(pt_1 >= 200) ) * ( (1-0.002*pt_2)*(pt_2 < 200) + 0.6*(pt_2 >= 200) ) )", ["pt_1","pt_2"])
                },
                "CMS_htt_jetToTauFake_Run2017Down"            :{
                   "et":Weight("((1+0.002*pt_2)*(pt_2 < 200) + 1.4*(pt_2 >= 200))", ["pt_2"]),
                   "mt":Weight("((1+0.002*pt_2)*(pt_2 < 200) + 1.4*(pt_2 >= 200))", ["pt_2"]),
                   "tt":Weight("(( (1+0.002*pt_1)*(pt_1 < 200) + 1.4*(pt_1 >= 200) ) * ( (1-0.002*pt_2)*(pt_2 < 200) + 1.4*(pt_2 >= 200) ) )", ["pt_1","pt_2"])
                },
                "CMS_scale_j_Run2017Up"                       : Weight("",[]),
                "CMS_scale_j_Run2017Down"                     : Weight("",[])                
            }
        },
        "lepton_fakes":{
            "apply_to":["ZL"],
            "weights":{
                "CMS_ZLShape_mt_1prong_Run2017Up"             : Weight("",[]),
                "CMS_ZLShape_mt_1prong_Run2017Down"           : Weight("",[]),
                "CMS_ZLShape_mt_1prong1pizero_Run2017Up"      : Weight("",[]),
                "CMS_ZLShape_mt_1prong1pizero_Run2017Down"    : Weight("",[]),
                "CMS_ZLShape_et_1prong_Run2017Up"             : Weight("",[]),
                "CMS_ZLShape_et_1prong_Run2017Down"           : Weight("",[]),
                "CMS_ZLShape_et_1prong1pizero_Run2017Up"      : Weight("",[]),
                "CMS_ZLShape_et_1prong1pizero_Run2017Down"    : Weight("",[]),        
                "CMS_mFakeTau_1prong_Run2017Up"               : Weight("",[]),
                "CMS_mFakeTau_1prong_Run2017Down"             : Weight("",[]),
                "CMS_mFakeTau_1prong1pizero_Run2017Up"        : Weight("",[]),
                "CMS_mFakeTau_1prong1pizero_Run2017Down"      : Weight("",[]),
                "CMS_eFakeTau_1prong_Run2017Up"               : Weight("",[]),
                "CMS_eFakeTau_1prong_Run2017Down"             : Weight("",[]),
                "CMS_eFakeTau_1prong1pizero_Run2017Up"        : Weight("",[]),
                "CMS_eFakeTau_1prong1pizero_Run2017Down"      : Weight("",[]) 
            }
        },
        "trigger_lepton_legs_mc":{
            "apply_to":["ZTT", "ZL", "ZJ", "W", "TTT", "TTL", "TTJ", "VVL", "VVT", "VVJ"] + signals,
            "weights":{
                "CMS_eff_trigger_mt_Run2017Up":             Weight("(1.0*(pt_1<=25)+1.02*(pt_1>25))",["pt_1"]),
                "CMS_eff_trigger_mt_Run2017Down":           Weight("(1.0*(pt_1<=25)+0.98*(pt_1>25))",["pt_1"]),
                "CMS_eff_xtrigger_mt_Run2017Up":            Weight("(1.054*(pt_1<=25)+1.0*(pt_1>25))",["pt_1"]),
                "CMS_eff_xtrigger_mt_Run2017Down":          Weight("(0.946*(pt_1<=25)+1.0*(pt_1>25))",["pt_1"]),
                "CMS_eff_trigger_et_Run2017Up":             Weight("(1.0*(pt_1<=28)+1.02*(pt_1>28))",["pt_1"]),
                "CMS_eff_trigger_et_Run2017Down":           Weight("(1.0*(pt_1<=28)+0.98*(pt_1>28))",["pt_1"]),
                "CMS_eff_xtrigger_et_Run2017Up":            Weight("(1.054*(pt_1<=28)+1.0*(pt_1>28))",["pt_1"]),
                "CMS_eff_xtrigger_et_Run2017Down":          Weight("(0.946*(pt_1<=28)+1.0*(pt_1>28))",["pt_1"]),
            }
        },
        "trigger_lepton_legs_emb":{
            "apply_to":["EMB"],
            "weights":{
                "CMS_eff_trigger_emb_mt_Run2017Up":             Weight("(1.0*(pt_1<=25)+1.02*(pt_1>25))",["pt_1"]),
                "CMS_eff_trigger_emb_mt_Run2017Down":           Weight("(1.0*(pt_1<=25)+0.98*(pt_1>25))",["pt_1"]),
                "CMS_eff_xtrigger_emb_mt_Run2017Up":            Weight("(1.054*(pt_1<=25)+1.0*(pt_1>25))",["pt_1"]),
                "CMS_eff_xtrigger_emb_mt_Run2017Down":          Weight("(0.946*(pt_1<=25)+1.0*(pt_1>25))",["pt_1"]),
                "CMS_eff_trigger_emb_et_Run2017Up":             Weight("(1.0*(pt_1<=28)+1.02*(pt_1>28))",["pt_1"]),
                "CMS_eff_trigger_emb_et_Run2017Down":           Weight("(1.0*(pt_1<=28)+0.98*(pt_1>28))",["pt_1"]),
                "CMS_eff_xtrigger_emb_et_Run2017Up":            Weight("(1.054*(pt_1<=28)+1.0*(pt_1>28))",["pt_1"]),
                "CMS_eff_xtrigger_emb_et_Run2017Down":          Weight("(0.946*(pt_1<=28)+1.0*(pt_1>28))",["pt_1"]),
            }
        },        
        "ggFWG1Uncertainties":{
            "apply_to": signals_ggh,
            "weights":{
                "THU_ggH_MuUp":       Weight("THU_ggH_Mu",["THU_ggH_Mu"] ),
                "THU_ggH_MuDown":     Weight("1.0 / THU_ggH_Mu",["THU_ggH_Mu"] ),
                "THU_ggH_ResUp":      Weight("THU_ggH_Res",["THU_ggH_Res"] ),
                "THU_ggH_ResDown":    Weight("1.0 / THU_ggH_Res",["THU_ggH_Res"] ),
                "THU_ggH_Mig01Up":    Weight("THU_ggH_Mig01",["THU_ggH_Mig01"] ),
                "THU_ggH_Mig01Down":  Weight("1.0 / THU_ggH_Mig01",["THU_ggH_Mig01"] ),
                "THU_ggH_Mig12Up":    Weight("THU_ggH_Mig12",["THU_ggH_Mig12"] ),
                "THU_ggH_Mig12Down":  Weight("1.0 / THU_ggH_Mig12",["THU_ggH_Mig12"] ),
                "THU_ggH_VBF2jUp":    Weight("THU_ggH_VBF2j",["THU_ggH_VBF2j"] ),
                "THU_ggH_VBF2jDown":  Weight("1.0 / THU_ggH_VBF2j",["THU_ggH_VBF2j"] ),
                "THU_ggH_VBF3jUp":    Weight("THU_ggH_VBF3j",["THU_ggH_VBF3j"] ),
                "THU_ggH_VBF3jDown":  Weight("1.0 / THU_ggH_VBF3j",["THU_ggH_VBF3j"] ),
                "THU_ggH_PT60Up":     Weight("THU_ggH_PT60",["THU_ggH_PT60"] ),
                "THU_ggH_PT60Down":   Weight("1.0 / THU_ggH_PT60",["THU_ggH_PT60"] ),
                "THU_ggH_PT120Up":    Weight("THU_ggH_PT120",["THU_ggH_PT120"] ),
                "THU_ggH_PT120Down":  Weight("1.0 / THU_ggH_PT120",["THU_ggH_PT120"] ),
                "THU_ggH_qmtopUp":    Weight("THU_ggH_qmtop",["THU_ggH_qmtop"] ),
                "THU_ggH_qmtopDown":  Weight("1.0 / THU_ggH_qmtop",["THU_ggH_qmtop"] )
            }
        }    
    }
}
