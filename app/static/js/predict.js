    $(document).ready(function(){

        
    // SIDEBAR FUNCTIONS 
        $('#explore').on('click', function(){
            $('.explore-collapse').slideToggle();
        });

        $('#analyze').on('click', function(){
            $('.analyze-collapse').slideToggle();
        });

        $('.advanced-toggle').on('click', function(){
            $('.advanced').slideToggle();
        });

    });
