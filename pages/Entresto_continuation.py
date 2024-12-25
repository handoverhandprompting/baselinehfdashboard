import streamlit as st
from models.util import ShowHR
from models.page_util import hr_cal


def second_page():
    st.subheader('Entresto continuation')
    if 'risk_value2_col1' not in st.session_state:
        st.session_state['risk_value2_col1'] = 1.0
    if 'risk_value2_col2' not in st.session_state:
        st.session_state['risk_value2_col2'] = 1.0
    if '_sync1n9' not in st.session_state:
        st.session_state['_sync1n9'] = False

    # For decrease eGFR level
    if 'egfr_list' not in st.session_state:
        st.session_state['efgr_list'] = []

    ShowHR(st.session_state['risk_value2_col1'], st.session_state['risk_value2_col2']).show()
    enter2_col1, enter2_col2 = st.columns(2)

    st.markdown('<style>div[data-testid="stExpander"] div[role="button"] p{font-weight: bold}</style>', unsafe_allow_html=True)


    with st.expander(':man-frowning: :violet[Baseline Status]'):
        dialysis_display = st.selectbox('Dialysis', [['No', False], ['Yes', True]], format_func=lambda x: x[0],)
        dialysis = dialysis_display[1]
        cad_display = st.selectbox('CAD', [['No', False], ['Yes', True]], format_func=lambda x: x[0], help='Coronary artery disease')
        cad = cad_display[1]
        hb_level = None
        hb_level_display = st.text_input('Hb level(g/dL)', help='Hemoglobin')
        if hb_level_display:
            try:
                hb_level = round(float(hb_level_display), 2)
            except:
                st.warning('請輸入數字')


    with st.expander(':pill: Baseline Drug Use'):
        nsaid_display = st.selectbox('NSAID',  [['No', False], ['Yes', True]], format_func=lambda x: x[0], help='Nonsteroidal anti-inflammatory drugs')
        nsaid = nsaid_display[1]
        antiplatelet_display = st.selectbox('Antiplatelet drugs', [['No', False], ['Yes', True]], format_func=lambda x: x[0], help='Drugs used for coronary artery disease')
        antiplatelet = antiplatelet_display[1]
        left_col, mid_col, right_col = st.columns([4, 3, 3])
        with left_col:
            ld_ = st.selectbox('Loop diuretics', ['None', 'furosemide', 'bumetanide'], help='1. PO equivalence: (F) 40 mg = (B) 1 mg\n 2. IV equivalence: (F) 20 mg = (B) 1 mg\n 3. (F): 40 mg PO = 20 mg IV\n 4. (F): furosemide; (B) bumetanide')
        with mid_col:
            second_ = st.selectbox('middle', ['IV', 'PO'], disabled=(ld_ == 'None'), label_visibility='hidden')
        with right_col:
            daily_dose_ = None
            daily_dose_display = st.text_input('Daily dose(mg)', disabled=(ld_ == 'None'))
            if daily_dose_display:
                try:
                    daily_dose_ = round(float(daily_dose_display))
                except:
                    st.warning('請輸入數字')

    with st.expander(':1234: Current Status'):
        current_hb = None
        current_hb_display = st.text_input('Hb level(g/dL)', help='Hemoglobin', key='current_hb_display')
        if current_hb_display:
            try:
                current_hb = round(float(current_hb_display))
            except:
                st.warning('請輸入數字')
        st.divider()

        egfr_decrease_display_list = []
        egfr_decrease_display0 = st.number_input('Maximum PERCENTAGE decrease of eGFR (mL/min/1.73 m2) in the past 3 months', step=0.01,
                                                 help='Enter estimated glomerular filtration rates in mL/min/1.73 m2 which will be automatically converted to a percentage')
        if egfr_decrease_display0:
            egfr_decrease_display_list += [egfr_decrease_display0]
            i = 1
            while True:
                if ('egfr_decrease_display' + str(i - 1)) in locals() and locals()['egfr_decrease_display' + str(i - 1)] is not None:
                    locals()['egfr_decrease_display' + str(i)] = st.number_input('Maximum PERCENTAGE decrease of eGFR (mL/min/1.73 m2) in the past 3 months', key=('e' + str(i)), value=None, label_visibility='hidden')
                    if locals()['egfr_decrease_display' + str(i)]:
                        egfr_decrease_display_list += [locals()['egfr_decrease_display' + str(i)]]
                    else:
                        break
                else:
                    break
                i += 1
        st.divider()

        bun_increase_display_list = []
        bun_increase9_display_list = []
        bun_increase_display0 = st.number_input('Maximum increase of BUN level (mg/dL) in the past 1 month', step=0.01, help='Blood urea nitrogen')
        if bun_increase_display0:
            bun_increase_display_list += [bun_increase_display0]
            i = 1
            while True:
                if ('bun_increase_display' + str(i - 1)) in locals() and locals()['bun_increase_display' + str(i - 1)] is not None:
                    locals()['bun_increase_display' + str(i)] = st.number_input('Maximum increase of BUN level (mg/dL) in the past 1 month', key=('b' + str(i)), value=None, label_visibility='hidden')
                    if locals()['bun_increase_display' + str(i)]:
                        bun_increase_display_list += [locals()['bun_increase_display' + str(i)]]
                    else:
                        break
                else:
                    break
                i += 1
        st.divider()

        st.write('Maximum increase of BUN level (mg/dL) in the past 9 month')
        if st.button('sync', key='1mon_sync'):
            st.session_state['_sync1n9'] = True
            fake_index = 0
            for fake_input_value in bun_increase_display_list:
                st.number_input('fake_input', key='fake_input' + str(fake_index), label_visibility='hidden', disabled=True, value=fake_input_value)
                fake_index += 1


        bun_increase9_display0 = st.number_input('Maximum increase of BUN level (mg/dL) in the past 9 month', step=0.01, help='Blood urea nitrogen', label_visibility='hidden')
        if bun_increase9_display0:
            bun_increase9_display_list += [bun_increase9_display0]
            i = 1
            while True:
                if ('bun_increase9_display' + str(i - 1)) in locals() and locals()['bun_increase9_display' + str(i - 1)] is not None:
                    locals()['bun_increase9_display' + str(i)] = st.number_input('Maximum increase of BUN level (mg/dL) in the past 9 month', key=('b9' + str(i)), value=None, label_visibility='hidden')
                    if locals()['bun_increase9_display' + str(i)]:
                        bun_increase9_display_list += [locals()['bun_increase9_display' + str(i)]]
                    else:
                        break
                else:
                    break
                i += 1
        if st.session_state['_sync1n9']:
            bun_increase9_display_list = bun_increase_display_list + bun_increase9_display_list

        st.divider()

        levf_list = []
        levf0 = st.number_input('Average LVEF(%)', step=0.01, help='Enter left ventricular ejection fractions estimated through the Teichholz method (M-mode), or values from 2D echocardiography (e.g., Simpson’s method) if unavailable.')
        if levf0:
            levf_list += [levf0]
            i = 1
            while True:
                if ('levf' + str(i - 1)) in locals() and locals()['levf' + str(i - 1)] is not None:
                    locals()['levf' + str(i)] = st.number_input('Enter left ventricular ejection fractions estimated through the Teichholz method (M-mode), or values from 2D echocardiography (e.g., Simpson’s method) if unavailable.', key=('le' + str(i)), value=None, label_visibility='hidden')
                    if locals()['levf' + str(i)]:
                        levf_list += [locals()['levf' + str(i)]]
                    else:
                        break
                else:
                    break
                i += 1
        st.divider()

        lvmi_list = []
        lvmi0 = st.number_input('Average LVMI (g/m2)', step=0.01, help='Left ventricular mass index', key='lv0')
        if lvmi0:
            lvmi_list += [lvmi0]
            i = 1
            while True:
                if ('lvmi' + str(i - 1)) in locals() and locals()['lvmi' + str(i - 1)] is not None:
                    locals()['lvmi' + str(i)] = st.number_input('Average LVMI (g/m2)', key=('lv' + str(i)), value=None, label_visibility='hidden')
                    if locals()['lvmi' + str(i)]:
                        levf_list += [locals()['lvmi' + str(i)]]
                    else:
                        break
                else:
                    break
                i += 1
        st.divider()

        lvedd = st.number_input('LVEDD (mm)', key='lvedd', help='Left ventricular end-diastolic diameter ')

    with st.expander(':microbe: Current Drug Use'):
        sv = st.number_input('Sacubitril/valsartan daily dose (mg)', key='sv')
        st.divider()

        nc_list = []
        nc0 = st.number_input('Nicorandil cumulative dose in the past 3 months (mg)', step=0.01, key='nc0')
        if nc0:
            nc_list += [nc0]
            i = 1
            while True:
                if ('nc' + str(i - 1)) in locals() and locals()['nc' + str(i - 1)] is not None:
                    locals()['nc' + str(i)] = st.number_input('icorandil cumulative dose in the past 3 months (mg)', key=('nc' + str(i)), value=None, label_visibility='hidden')
                    if locals()['nc' + str(i)]:
                        nc_list += [locals()['nc' + str(i)]]
                    else:
                        break
                else:
                    break
                i += 1

    st.markdown("""
                <style>.element-container:has(#button-col2) + div button {
                 background-color: #ff0000;
                        color: #ffffff;
                 }</style>""", unsafe_allow_html=True)
    st.markdown("""
                <style>.element-container:has(#button-col1) + div button {
                 background-color: #0000ff;
                        color: #ffffff;
                 }</style>""", unsafe_allow_html=True)
    with enter2_col1:
        st.markdown('<span id="button-col1"></span>', unsafe_allow_html=True)

        btn_left = st.button('Enter', key='btn_left', on_click=hr_cal, args=(dialysis, cad, hb_level, nsaid, antiplatelet, ld_, second_, daily_dose_, current_hb,
                                                                             egfr_decrease_display_list, bun_increase_display_list, bun_increase9_display_list, levf_list, lvmi_list,
                                                                             lvedd, sv, nc_list, 'risk_value2_col1'))
    with enter2_col2:
        st.markdown('<span id="button-col2"></span>', unsafe_allow_html=True)

        btn_right = st.button('Enter', key='btn_right', on_click=hr_cal, args=(dialysis, cad, hb_level, nsaid, antiplatelet, ld_, second_, daily_dose_, current_hb,
                                                                               egfr_decrease_display_list, bun_increase_display_list, bun_increase9_display_list, levf_list, lvmi_list,
                                                                               lvedd, sv, nc_list, 'risk_value2_col2'))


if __name__ == '__main__':
    second_page()
