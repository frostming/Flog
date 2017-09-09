// JavaScript Document

$('.tipW').tipsy({
	title: 'title',
	trigger: 'hover',
	html: true,
	gravity: 'e'
});

$('.tipN').tipsy({
	title: 'title',
	trigger: 'hover',
	html: true,
	gravity: 's'
});

$('.tipNDelay').tipsy({
	title: 'title',
	trigger: 'hover',
	html: true,
	gravity: 's',
	delayIn: 1000,
	fade: true
});