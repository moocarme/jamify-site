
var applicature          = {"Cadd9":[{"l":[],"x":0,"n":[52,48,43,38,36,-1],"t":[0,1,0,0,3,-1],"g":[0,1,0,0,3,0],"f":0}],"D":[{"l":[],"x":2,"n":[54,50,45,38,-1,-1],"t":[2,3,2,0,-1,-1],"g":[2,3,1,0,0,0],"f":0}],"Em7":[{"l":[],"x":4,"n":[52,47,43,38,35,28],"t":[0,0,0,0,2,0],"g":[0,0,0,0,1,0],"f":0}]};

var acc_tuning           = "E A D G B E";
var appl_api_version     = 3;

function(e) {
  $chord.addClass("has_undragable");
  var ch = $chord.text(),
    $widget = create_applicature_widget(ch, acc_tuning, {
      vars_left: !1
    });
  return display_widget($widget, $chord, !0), !1
}


function create_applicature_widget(chord,tuning,options){
	var $widget=null,
	html=render_applicature(chord,tuning,options);

	return $widget=html?$(html):$("")
}

function render_applicature(chord,tuning,options){
	options=$.extend({count_class:""},options);
	var html=null;
	if(chord=Chord.convertChordName(chord),void 0!==Chord.convertChordName(chord)){
		var applicature_item=applicature[chord],
		vars_list=build_variations_list(applicature_item,tuning);
		html+='<div class="chord-variations-wrapper '+options.count_class+'">',
		html+=render_head(chord),html+='<div class="diagwrap">',
		html+='<div class="main_chord_with_play"><div class="play-on-hover"><b><i></i><span>hover to play</span></b>',
		html+='<div class="cont_chrd" rel="0">',vars_list.length&&(html+=vars_list[0]),
		html+="</div>",html+="</div></div>",
		html+='<div class="varctrl">variations</div>',
		html+='<div class="chords_versions_handler">',
		html+=render_variations_list(vars_list),
		html+=render_variations_controls(vars_list),
		html+="</div>",html+="</div>",
		html+="</div>"}
		return html
}

function build_variations_list(appls,tuning){
	var list=[],vars_count=0;
	for(var i in appls){
		var applicature_item=appls[i];
		if("suggested_fret"!=i&&"old_ch"!=i&&"_"!=i.substring(0,1)){
			vars_count++;
			var html="";
			html+='<div class="chfret">',
			html+=1==vars_count?'<div class="chfret_clicked_label" style="display: block;"></div>':'<div class="chfret_clicked_label"></div>',
			html+=render_play_link(applicature_item);
			for(var capoIndex=0; capoIndex<applicature_item.l.length; capoIndex++)
			html+=render_capo(applicature_item.l[capoIndex].f-applicature_item.f+(0==applicature_item.f?0:1),applicature_item.l[capoIndex].e);
			for(var string=0;string<applicature_item.t.length;string++)
			applicature_item.g[string]>0&&(html+=render_finger(string,applicature_item.t[string]-applicature_item.f+(0==applicature_item.f?0:1),applicature_item.g[string]));
			html+=render_tuning(tuning),
			html+=render_strings(find_bass_string(applicature_item),applicature_item),
			html+="</div>",html+=render_fret(applicature_item),list.push(html)}}
	return list
}

function render_variations_list(vars_list){
	var html='<div class="chords_versions_handler_limiter">';
	html+='<div class="chords_versions_scroller_moveable" rel="1">';
	for(var i=0;i<vars_list.length;i++)
	html+='<div class="cont_chrd" rel="'+i+'">'+vars_list[i]+"</div>";
	return html+="</div>",html+="</div>"
}

function render_play_link(applicature_item){
	var html="";
	return html+='<a class="p_apl play_applicature_button" rel="'+prepareNotesString(applicature_item.n)+'" href="#"></a>'
}

function render_strings(bass_string,applicature_item){
	for(var html='<div class="strings">',string=0;string<applicature_item.t.length;string++)
	html+=render_string(string,bass_string,applicature_item.t[string]);
	return html+="</div>"
}

function render_string(string,bass_string,fret){
	var string_class="f-str";
	return-1==fret?string_class="x-str":0==fret&&(string_class="o-str"),'<div class="'+string_class+'" rel="string'+string+" bass"+bass_string+'"></div>'
}

function render_variations_controls(vars_list){
	var html='<div class="chords_versions_controls">';
	return html+='<div class="chords_versions_controls_left"><b></b> Prev</div>',
	html+='<div class="chords_versions_controls_info_text">',html+="1 of "+Math.ceil(vars_list.length/2),
	html+="</div>",vars_list.length>2&&(html+='<div class="chords_versions_controls_right">Next <b></b></div>'),html+="</div>"
}

function render_capo(fret,lastString){
	return'<div class="barre finger-fret-'+fret+" capo-string-"+lastString+'"></div>'
}

function render_finger(string,fret,finger){
	return fret<0?"":'<div class="fingbg finger-string-'+string+" finger-fret-"+fret+'"><div class="f-'+finger+'"></div></div>'
}

function render_fret(applicature_item){
	var fret_tmp="&nbsp;";0!=applicature_item.f&&(fret_tmp=applicature_item.f+" fr");
	var html='<div class="fs-10 fretnum">'+fret_tmp+"</div>";
	return html
}