var simplemde = new SimpleMDE({
  element: $("[data-role='mdeditor']")[0],
  autosave: {
    enabled: true,
    uniqueId: 'new-post',
    delay: 30000,
  },
  spellChecker: false
});

$('select[data-role=select2]').select2({
  tags: true
})
