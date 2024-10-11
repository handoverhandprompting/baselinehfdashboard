import streamlit as st
from models.util import calculate_and_set, predict_plot


# ==========
def prediction_view():
    st.subheader('Survival Prediction')
    if 'risk_value_col1_pred' not in st.session_state:
        st.session_state['risk_value_col1_pred'] = 1.0
        hr1 = st.session_state['risk_value_col1_pred']

    else:
        hr1 = st.session_state['risk_value_col1_pred']

    if 'risk_value_col2_pred' not in st.session_state:
        st.session_state['risk_value_col2_pred'] = 1.0
        hr2 = st.session_state['risk_value_col2_pred']
    else:
        hr2 = st.session_state['risk_value_col2_pred']

    # plotting
    prediction = predict_plot(hr1, hr2)
    st.pyplot(prediction)

    # place the holder here
    enter_col1, enter_col2 = st.columns(2)

    # Hight, weight and BMI
    with st.expander(':man-frowning: :violet[Baseline status]'):
        age = st.number_input('Age', step=1, key='age_pred')
        bmi = 0
        col1, col1_1, col2, col2_2 = st.columns([5, 2, 5, 2])
        with col1_1:
            height_unit = st.selectbox("Height_unit", ["cm", "in"], key='hight-unit_pred')
        with col2_2:
            weight_unit = st.selectbox("Weight_unit", ["kg", "lbs"], key='weight-unit_pred')
        with col1:
            height = st.number_input('Height ', step=1, value=160, key='height_pred')
            if height:
                if height_unit == "in":
                    height = height * 2.54
        with col2:
            weight = st.number_input('Weight ', step=1, value=60, key='weight_pred')
            if weight:
                if weight_unit == "lbs":
                    weight = weight * 0.45359237
        if height and weight:
            bmi = round(weight / ((height / 100) ** 2), 2)

        col1, col2, col3 = st.columns([1, 3, 4])
        with col1:
            st.markdown('BMI: ')
            with col2:
                if bmi is not None:
                    st.markdown(str(bmi))

    with st.expander("😷 :blue[Disease status]"):

        col1, col2 = st.columns(2)
        with col1:
            nyha_display = st.selectbox('NYHA', [['None/Unclassified', 0],
                                                 ['Class I (No limitation of physical activity. Ordinary physical activity does not cause undue fatigue, palpitation or shortness of breath.)', 1],
                                                 ['Class II (Slight limitation of physical activity. Comfortable at rest. Ordinary physical activity results in fatigue, palpitation, shortness of breath or chest pain.)', 2],
                                                 ['Class III (Marked limitation of physical activity. Comfortable at rest. Less than ordinary activity causes fatigue, palpitation, shortness of breath or chest pain.)', 3],
                                                 ['Class IV (Symptoms of heart failure at rest. Any physical activity causes further discomfort.)', 4]], format_func=lambda x: x[0],
                                        help='New York Heart Association functional classification', index=0, key='nyha_display_pred')
            nyha = nyha_display[1]
            paod_diplay = st.selectbox('PAOD', [['yes', 1], ['no', 0]], format_func=lambda x: x[0], index=1, help='Peripheral Arterial Occlusive Disease', key='paod_diplay_pred')
            paod = paod_diplay[1]
        with col2:
            dialysis_display = st.selectbox('Dialysis', [['yes', 1], ['no', 0]], format_func=lambda x: x[0], index=1, key='dialysis_display_pred')
            dialysis = dialysis_display[1]

    # st.write('---')
    with st.expander(':pill: Drug use'):
        col1, col2 = st.columns([5, 2])
        with col1:
            acei_display = st.selectbox('ACEI/ARB',
                                        ['None', 'valsartan', 'losartan', 'captopril', 'enalapril', 'ramipril', 'Not mentioned above'],
                                        help='Angiotensin Converting Enzyme Inhibitors/Angiotensin Receptor Blockers', index=0, key='acei_display_pred')
        with col2:
            acei_dose = st.number_input('Dose(mg)', disabled=(acei_display == 'None' or acei_display == 'Not mentioned above'), value=None, key='acei_dose_pred')
            if acei_dose:
                if acei_display == 'Valsartan':
                    total_acei = acei_dose
                elif acei_display == 'Losartan' or acei_display == 'Captopril':
                    total_acei = acei_dose * 32 / 15
                elif acei_display == 'Enalapril':
                    total_acei = acei_dose * 16
                elif acei_display == 'Ramipril':
                    total_acei = acei_dose * 32
                else:
                    total_acei = 0
            else:
                total_acei = 141

        col1, col2 = st.columns(2)
        with col1:
            en_h_display = st.selectbox('Initiation time of Entresto(sacubitril/valsartan)',
                                        ['Outpatient Department (OPD)', 'Inpatient Department (IPD)', 'None'], key='en_h_display_pred')
        with col2:
            ua_u_o_display = st.selectbox('Urate-lowering Agents', ['None', 'allopurinol', 'benzbromarone', 'febuxostat', 'probenecid', 'rasburicase', 'sulfinpyrazone', 'Not mentioned above'], index=0, key='ua_u_o_display_pred')
            if ua_u_o_display == 'None' or ua_u_o_display == 'Not mentioned above':
                ua_u_0 = 0
            else:
                ua_u_0 = 1
        col1, col2 = st.columns(2)
        with col1:
            p2y12_display = st.selectbox('P2Y12 Receptor Inhibitors', ['None', 'clopidogrel', 'prasugrel', 'ticagrelor', 'Not mentioned above'], index=0, key='p2y12_display_pred')
            if p2y12_display == 'None' or p2y12_display == 'Not mentioned above':
                p2y12 = 0
            else:
                p2y12 = 1

    with st.expander('🩸 :orange[Lab data]'):
        with st.container():
            col1, col1_1, space, col2, col3 = st.columns([3, 6, 3, 3, 6])
            with col1:
                st.write(f'###### BUN ######')
                bun_none = st.checkbox('None', key='bun_none_pred', value=True)
            with col1_1:
                bun = st.number_input('(mg/dL)', disabled=bun_none, help='Blood Urea Nitrogen', value=20, key='bun_pred')

            with col2:
                st.write(f'###### NT_proBNP ######')
                nt_proBNP_none = st.checkbox('None', key='nt_proBNP_none_pred', value=True)
            with col3:
                nt_proBNP = st.number_input('(pg/mL)', disabled=nt_proBNP_none, help='N-Terminal Pro-Brain (or B-type) Natriuretic Peptide', value=750, key='nt_proBNP_pred')

        st.write(' ')

        with st.container():
            col1, col1_1, space1, col2, col2_1 = st.columns([3, 6, 3, 3, 6])
            with col1:
                st.write(f'###### ALT ######')
                alt_none = st.checkbox('None', key='alt_none_pred', value=True)
            with col1_1:
                alt = st.number_input('(U/L)', disabled=alt_none, key='alt_pred', help='Alanine Aminotransferase', value=20.3)

            with col2:
                st.write(f'###### RDW_CV ######')
                rdw_cv_none = st.checkbox('None', key='rdw_cv_none_pred', value=True)
            with col2_1:
                rdw_cv = st.number_input('(%)', disabled=rdw_cv_none, key='rdw_cv_pred', help='Red Cell Distribution Width_Coefficient of Variation', value=15.5)

    with st.expander('❤️ :red[Cardiac parameters of echocardiography]'):
        with st.container():
            col1, col1_1, space1, col2, col2_1 = st.columns([3, 6, 3, 3, 6])
            with col1:
                st.write(f'###### AR ######')
                ar_none = st.checkbox('None', key='ar_none_pred', value=True)
            with col1_1:
                ar = st.selectbox(' ', [['trace/trivial', 0.5], ['mild', 1], ['mild to moderate', 1.5], ['moderate', 2],
                                        ['moderate to severe', 2.5], ['severe', 3]], label_visibility='visible', disabled=ar_none, help='Aortic Regurgitation', format_func=lambda x: x[0], key='ar_pred')
                ar_value = ar[1]
            with col2:
                st.write(f'###### RV ######')
                rvdd_none = st.checkbox('None', key='rvdd_none_pred', value=True)
            with col2_1:
                rvdd = st.number_input('(cm)', key='rvdd_pred', disabled=rvdd_none, help='RVDd, Right Ventricular Diastolic Dimension', value=3.5)

        with st.container():
            col1, col1_1, space1, col2, col2_1 = st.columns([3, 6, 3, 3, 6])
            with col1:
                st.write(f'###### IVSd ######')
                ivsd_none = st.checkbox('None', key='ivsd_none_pred', value=True)
            with col1_1:
                ivsd = st.number_input('(cm)', key='ivsd_pred', disabled=ivsd_none, help='Interventricular Septum Dimension', value=1.5)

            with col2:
                st.write(f'###### LVMI ######')
                lvmi_none = st.checkbox('None', key='lvmi_none_pred', value=True)
            with col2_1:
                lvmi = st.number_input('(g/m2)', key='lvmi_pred', disabled=lvmi_none, label_visibility='visible', help='Left Ventricular Mass Index', value=150.5)

        with st.container():
            col1, col1_1, space1, col2, col2_1 = st.columns([3, 6, 3, 3, 6])
            with col1:
                st.write(f'###### ESD ######')
                esd_none = st.checkbox('None', key='esd_none_pred', value=True)
            with col1_1:
                esd = st.number_input('(cm)', key='esd_pred', disabled=esd_none, help='End Systolic Dimension = LVIDs, Left Ventricular Internal Diameter End Systole', value=5.5)

            with col2:
                st.write(f'###### LAD ######')
                lad_none = st.checkbox('None', key='lad_none_pred', value=True)
            with col2_1:
                lad = st.number_input('(cm)', key='lad_pred', disabled=lad_none, label_visibility='visible', help='LAD, Left Atrial Diameter', value=4.35)

        with st.container():
            col1, col1_1, space1, col2, col2_1 = st.columns([3, 6, 3, 3, 6])
            with col1:
                st.write(f'###### LVEF_2D ######')
                lvef_2d_none = st.checkbox('None', key='lvef_2d_none_pred', value=True)
            with col1_1:
                lvef_2d = st.number_input('(%)', key='lvef_2d_pred', disabled=lvef_2d_none, label_visibility='visible', help='Left Ventricular Ejection Fraction_2D = EF MOD-sp4, Ejection Fraction Method of Disks-Single Plane, Apical 4 Chamber', value=35.5)
    # TODO:Change button layout

    # Assign what shall do in enter_col1 and enter_col2
    st.markdown("""
<style>.element-container:has(#button-col1) + div button {
 background-color: #0000ff;
        color: #ffffff;
 }</style>""", unsafe_allow_html=True)
    with enter_col1:
        st.markdown('<span id="button-col1"></span>', unsafe_allow_html=True)
        st.button('Enter', 'enter1_pred', on_click=calculate_and_set, args=(
            dialysis, bun, age, lvef_2d_none, lvef_2d, esd_none, esd, rdw_cv_none, rdw_cv, ivsd_none, ivsd, bmi, lvmi_none, lvmi, nt_proBNP_none, nt_proBNP, paod, total_acei, p2y12, ar_none, ar_value, en_h_display, nyha, rvdd_none, rvdd, ua_u_0, alt_none, alt, lad_none, lad, 'risk_value_col1_pred'),
                  type='primary')

    st.markdown("""
<style>.element-container:has(#button-col2) + div button {
 background-color: #ff0000;
        color: #ffffff;
 }</style>""", unsafe_allow_html=True)
    with enter_col2:
        st.markdown('<span id="button-col2"></span>', unsafe_allow_html=True)
        st.button('Enter', 'enter2_pred', on_click=calculate_and_set, args=(
            dialysis, bun, age, lvef_2d_none, lvef_2d, esd_none, esd, rdw_cv_none, rdw_cv, ivsd_none, ivsd, bmi, lvmi_none, lvmi, nt_proBNP_none, nt_proBNP, paod, total_acei, p2y12, ar_none, ar_value, en_h_display, nyha, rvdd_none, rvdd, ua_u_0, alt_none, alt, lad_none, lad, 'risk_value_col2_pred'),
                  type='secondary')
