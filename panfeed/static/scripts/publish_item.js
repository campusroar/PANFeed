function PublishItemCtrl($scope)
{
    $scope.item;
    $scope.loading = false;
    $scope.loaded = false;

    $scope.convertURL = function()
    {
        var converter_url = "/urltoitem";
        jQuery.ajax(
        { 
            url:converter_url,
            data: { url:$scope.url },
            dataType:"json",
            async: false,
            beforeSend: function(xhr, status) 
            {
                $scope.loading = true;
            },
            success: function(data, status,request)
            {
                data.url = $scope.url;
                $scope.item = data;
                $scope.loaded = true;
                $scope.loading = false;
            }
        });
    };

    $scope.fetch = function(item_id)
    {
        $http(
        {
            method: "GET",
            url: '/api/v2/feeditem/?format=json&limit=1&id='+item_id,
            cache: $templateCache,
            transformResponse: function(data,headersGetter)
            {
                return JSON.parse(data).objects;
            }
        }).success(function(data,status)
        {
            $scope.item = data;
        });
     }
    console.log($scope.id);
    if($scope.id != undefined)
    {
        $scope.fetch($scope.id);
    }
}
