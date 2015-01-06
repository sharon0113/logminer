  $(document).ready(function() {
      function nameselect(name) {
          switch (name) {
              case '141216chdzj':
                  return "吃货的自觉";
                  break;
              case '141216dsmn':
                  return "搭讪美女";
                  break;
              case '141216gspk':
                  return "歌神PK";
                  break;
              case '141216sldzw':
                  return "失恋的滋味";
                  break;
              case '141216wmqkq':
                  return "我们看球去";
                  break;
              case '141216zghgm':
                  return "中国好闺蜜";
                  break;

              default:
                  return "";
                  break;
          }
      }
      $("#manhua").click(function() {
          $('#cartoon_list').html('')
          $.getJSON('/cartoon', function(data) {
              var list = "";
              for (index in data) {
                  var name = nameselect(index)
                  var tr = "<tr>" + "<td>" + name + "</td>" + "<td>" + data[index] + "</td>" + "</tr>"
                  list += tr;
              }
              $("#cartoon_list").append(list);
          })
      })

  })
