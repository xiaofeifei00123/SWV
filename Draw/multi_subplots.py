
    def draw_multiple_subplots(self, ds, picture_dic):
        """
        画一个多图, 6张， 一个站点的
        多子图
        Args:
            根据ds来绘图
            model_dic ([type]): 各试验数据的字典
            负责绘图，就只负责绘图就好了，可以不用负责保存图片
        """

        fig = plt.figure(figsize=(10, 15), dpi=200)  # 创建页面
        grid = plt.GridSpec(4,
                            2,
                            figure=fig,
                            left=0.10,
                            right=0.98,
                            bottom=0.15,
                            top=0.93,
                            wspace=0.3,
                            hspace=0.35)

        num = 7
        axes = [None] * num
        # axes = [None] * 14  # 设置一个维度为8的空列表
        for i in range(num):
            axes[i] = fig.add_subplot(grid[i])

        model_list = ['ACM2', 'YSU', 'QNSE', 'QNSE_EDMF', 'TEMF', 'micaps', 'fnl']
        ax6 = fig.add_axes([0.2, 0.06, 0.7, 0.02])  # 重新生成一个新的坐标图

        var = str(ds.variable.values)
        time_select = str(ds.time[0].dt.hour.values)

        for i in range(len(model_list)):
            CS = None
                    # time_index = model_dic[model_list[i]].time.sel(time=datetime.time(12))
            CS = self.draw_contourf_single(axes[i],
                                            ds[model_list[i]], 
                                            )

            # title = str(station['name']) + "_" + model_list[i] + \
            #                 "_" + str(var)+"_"+str(time_select)
            # title = picture_dic['title'] + "_" + model_list[i]
            title = model_list[i]
            if model_list[i] == 'micaps':
                title = 'OBS'
            elif model_list[i] == 'fnl':
                title = 'FNL'
            axes[i].set_title(title, fontsize=14, loc='left')
        # plt.show()
            cb = fig.colorbar(CS,
                              cax=ax6,
                              orientation='horizontal',
                              shrink=0.8,
                              pad=0.14,
                              fraction=0.14)  # 这里的cs是画填色图返回的对象



