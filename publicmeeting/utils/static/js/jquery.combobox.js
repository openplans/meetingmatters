(function($) {
  $.widget( "ui.combobox", {
    _create: function() {
      var self = this,
        select = this.element.hide(),
        selected = select.children( ":selected" ),
        value = selected.val() ? selected.text() : "";
      var input = this.input = $( "<input>" )
        .insertAfter( select )
        .val( value )
        .autocomplete({
          delay: 0,
          minLength: 0,
          source: function( request, response ) {
            var matcher = new RegExp( $.ui.autocomplete.escapeRegex(request.term), "i" );
            response( select.children( "option" ).map(function() {
              var label = '', value = '';

              if (self.options.data) {
                var pk = $( this ).attr('value');
                var data = self.options.data[pk]
                if (data) {
                  label = data.label;
                  value = data.value;
                }
              } else {
                var text = $( this ).text();
                label = text
                value = text
              }

              if ( this.value && ( !request.term || matcher.test(label) ) )
                return {
                  label: label.replace(
                    new RegExp(
                      "(?![^&;]+;)(?!<[^<>]*)(" +
                      $.ui.autocomplete.escapeRegex(request.term) +
                      ")(?![^<>]*>)(?![^&;]+;)", "gi"
                    ), "<strong>$1</strong>" ),
                  value: value,
                  option: this
                };
            }) );
          },
          select: function( event, ui ) {
            ui.item.option.selected = true;
            select.trigger( "select", ui.item.option);
          },
          change: function( event, ui ) {
            if ( !ui.item ) {
              var matcher = new RegExp( "^" + $.ui.autocomplete.escapeRegex( $(this).val() ) + "$", "i" ),
                valid = false;
              select.children( "option" ).each(function() {
                if ( $( this ).text().match( matcher ) ) {
                  this.selected = valid = true;
                  return false;
                }
              });
              if ( !valid ) {
                // remove invalid value, as it didn't match anything
                $( this ).val( "" );
                select.val( "" );
                input.data( "autocomplete" ).term = "";
                select.trigger( "select" );
                return false;
              }
            }
            select.trigger( "change", ui.item.option);
          }
        }).addClass('span4');

      input.data( "autocomplete" )._renderItem = function( ul, item ) {
        return $( "<li></li>" )
          .data( "item.autocomplete", item )
          .append( "<a>" + item.label + "</a>" )
          .appendTo( ul );
      };
    },

    destroy: function() {
      this.input.remove();
      this.element.show();
      $.Widget.prototype.destroy.call( this );
    }
  });
})(jQuery);
