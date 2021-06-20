rankSS_txt = 'NX RiZE'
rankS_txt = 'Akw DL GK Marf Ri SrX VI Zw xer χer'
rankA_txt = "Vse NvK XV 25 いろはす St D-6 Nautilus D'e GX Exe NR Ap SGT FV Gw"
rankB_txt = "たまげた AKA  7st Stv FtS Valkyrie A'F GzK おれんじ Sy PAG IGS Res Sun w'nd ともしび LnP SH GTO L.D Cra Ar CoR MzE KSR"
rankC_txt = 'Amb MNG Shy おかし LN Ctw iZoNe Pss JxS Rnm Xan NV SFH SFH∞ IsK Unis Hw Lv OO Atelier HvG Vortex Vørtex Cr. Axe にゃんぱす Eins ZR Axis'
rankD_txt = 'AHW Rw KMC Rainbow くだもの PK Ass WiNG Null Reg SqV アフロ HiG VL MtG 360 LDH sf ET KZS zzZ φЯ φR'
rankE_txt = "Rov Rφ f's MG Frp Fun Mx0 NGZ LsV RsT FD LiT ペンギン Code zaru IZ TRB TIJ WM CrN Caf StN ￠ν ¢ν YaQ DZW DMs 6-R STD noir. noir Flower"
rankF_txt = "XYZ Spica Air Ocean BKN ちゅわん Nyn PHJ 旧帝大 Ly noel etoile Ez. Ez AgS Niz ポインコ Cry Per Vrost aristole Lav MaT NRZ PGS Pal Bijou Viola Sig Azu Mnk Trl MS TKY Mef MYT ATC kimi Vel HNT ΣX MoR FKZ PVU AIC USR Pd nk Lgt えもん XcR SR AFC Sat NGFC MkG By OP BS λ Gloria Osn CAJ SV FJI HhI ベイベ ENJ IXA サムライ VX Spring"
rankG_txt = "りん ごはん RED KM RsK GrL Gyof Sna Astra CoP WoU D&P level MM LTC LPN Dsy Roxane BP med Ash みけねこ γ's SN ToD TuR WU Cp うどん NKW LCP PN MCB Kas sng DFF Rc SKT us"
rankH_txt = "on EW MR Lr つきみ βiμ KNP εzK UMA IFU Syn xk Isn fate R! SHR YSN 3LT Rry ZK KC Q10 Mtp ちょこ IGi"
rankSS = list(rankSS_txt.split())
rankS = list(rankS_txt.split())
rankA = list(rankA_txt.split())
rankB = list(rankB_txt.split())
rankC = list(rankC_txt.split())
rankD = list(rankD_txt.split())
rankE = list(rankE_txt.split())
rankF = list(rankF_txt.split())
rankG = list(rankG_txt.split())
rankH = list(rankH_txt.split())
teamrank_dict = {'RANKSS':rankSS,'RANKS':rankS,'RANKA':rankA,'RANKB':rankB,'RANKC':rankC,'RANKD':rankD,'RANKE':rankE,'RANKF':rankF,'RANKG':rankG,'RANKH':rankH}

def rank(arg):
    arg_tmp = arg.upper()
    if len(arg_tmp) < 3:
        arg_tmp = 'RANK' + arg_tmp
    if arg_tmp in teamrank_dict:
        l = []
        for t in teamrank_dict[arg_tmp]:
            if t in ['SFH','φR','¢ν','noir','Ez','Vortex']:
                continue
            l.append(t)
        return ' '.join(l)
    for rank, teams in teamrank_dict.items():
        if arg in teams:
            return str('Rank ') + rank[4:]
    return False
